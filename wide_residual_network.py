from keras.models import Model
from keras.layers import Input, Add, Activation, Dropout, Flatten, Dense, Multiply, Lambda
from keras.layers.convolutional import Convolution2D, MaxPooling2D, AveragePooling2D
from keras.layers import BatchNormalization
from keras.regularizers import l2
from keras import backend as K
import numpy as np

weight_decay = 0.0005


def initial_conv(input):
    x = Convolution2D(16, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(input)

    channel_axis = 1 if K.image_data_format() == "channels_first" else -1

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    return x


def expand_conv(init, base, k, strides=(1, 1)):
    # Define trainable parameters for gamma and velocity
    gamma = K.variable(value=[0.9], dtype='float32', name='gamma')
    vel = K.variable(value=[0.0], dtype='float32', name='velocity')
    # gamma = 0.9
    # vel = 0.0

    x = Convolution2D(base * k, (3, 3), padding='same', strides=strides, kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(init)

    channel_axis = 1 if K.image_data_format() == "channels_first" else -1

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)

    x = Convolution2D(base * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    skip = Convolution2D(base * k, (1, 1), padding='same', strides=strides, kernel_initializer='he_normal',
                         kernel_regularizer=l2(weight_decay),
                         use_bias=False)(init)

    # Velocity
    gamma_vel = Multiply()([gamma, vel])  # gamma * vel
    complementary_gamma = Lambda(lambda ele: 1.0 - ele)(gamma)  # (1 - gamma)
    # gamma_vel = gamma * vel
    # complementary_gamma = 1 - gamma
    gamma_x = Multiply()([complementary_gamma, x])  # (1 - gamma)f(x)

    v = Add()([gamma_vel, gamma_x])  # gamma * vel + (1-gamma)f(x)

    m = Add()([v, skip])

    return m


def conv1_block(input, k=1, dropout=0.0):
    init = input

    # Define trainable parameters for gamma and velocity
    gamma = K.variable(value=[0.9], dtype='float32', name='gamma')
    vel = K.variable(value=[0.0], dtype='float32', name='velocity')
    # gamma = 0.9
    # vel = 0.0

    channel_axis = 1 if K.image_data_format() == "channels_first" else -1

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(input)
    x = Activation('relu')(x)
    x = Convolution2D(16 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    if dropout > 0.0:
        x = Dropout(dropout)(x)

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    x = Convolution2D(16 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    # Velocity
    # gamma_vel = Multiply()([gamma, vel]) # gamma * vel
    # complementary_gamma = Lambda(lambda ele: 1.0 - ele)(gamma) # (1 - gamma)
    gamma_vel = gamma * vel
    complementary_gamma = 1 - gamma
    gamma_x = Multiply()([complementary_gamma, x])  # (1 - gamma)f(x)
    v = Add()([gamma_vel, gamma_x])  # gamma * vel + (1-gamma)f(x)

    m = Add()([init, v])
    return m


def conv2_block(input, k=1, dropout=0.0):
    init = input

    # Define trainable parameters for gamma and velocity
    # gamma = K.variable(value=np.random.rand(1,1), dtype='float32', name='gamma')
    # vel = K.variable(value=np.random.rand(1,1), dtype='float32', name='velocity')
    gamma = K.variable(value=[0.9], dtype='float32', name='gamma')
    vel = K.variable(value=[0.0], dtype='float32', name='velocity')
    # gamma = 0.9
    # vel = 0.0

    channel_axis = 1 if K.image_data_format() == "th" else -1

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(input)
    x = Activation('relu')(x)
    x = Convolution2D(32 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    if dropout > 0.0:
        x = Dropout(dropout)(x)

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    x = Convolution2D(32 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    # Velocity
    # gamma_vel = Multiply()([gamma, vel]) # gamma * vel
    # complementary_gamma = Lambda(lambda ele: 1.0 - ele)(gamma) # (1 - gamma)
    gamma_vel = gamma * vel
    complementary_gamma = 1 - gamma
    gamma_x = Multiply()([complementary_gamma, x])  # (1 - gamma)f(x)

    v = Add()([gamma_vel, gamma_x])  # gamma * vel + (1-gamma)f(x)

    m = Add()([init, v])

    return m


def conv3_block(input, k=1, dropout=0.0):
    init = input

    # Define trainable parameters for gamma and velocity
    # gamma = K.variable(value=np.random.rand(1,1), dtype='float32', name='gamma')
    # vel = K.variable(value=np.random.rand(1,1), dtype='float32', name='velocity')
    # gamma = 0.9
    # vel = 0.0
    gamma = K.variable(value=[0.9], dtype='float32', name='gamma')
    vel = K.variable(value=[0.0], dtype='float32', name='velocity')

    channel_axis = 1 if K.image_data_format() == "th" else -1

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(input)
    x = Activation('relu')(x)
    x = Convolution2D(64 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    if dropout > 0.0:
        x = Dropout(dropout)(x)

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)
    x = Convolution2D(64 * k, (3, 3), padding='same', kernel_initializer='he_normal',
                      kernel_regularizer=l2(weight_decay),
                      use_bias=False)(x)

    # Velocity
    # gamma_vel = Multiply()([gamma, vel]) # gamma * vel
    # complementary_gamma = Lambda(lambda ele: 1.0 - ele)(gamma) # (1 - gamma)
    gamma_vel = gamma * vel
    complementary_gamma = 1 - gamma
    gamma_x = Multiply()([complementary_gamma, x])  # (1 - gamma)f(x)

    v = Add()([gamma_vel, gamma_x])  # gamma * vel + (1-gamma)f(x)

    m = Add()([init, v])

    return m


def create_wide_residual_network(input_dim, nb_classes=100, N=2, k=1, dropout=0.0, verbose=1):
    """
    Creates a Wide Residual Network with specified parameters

    :param input: Input Keras object
    :param nb_classes: Number of output classes
    :param N: Depth of the network. Compute N = (n - 4) / 6.
              Example : For a depth of 16, n = 16, N = (16 - 4) / 6 = 2
              Example2: For a depth of 28, n = 28, N = (28 - 4) / 6 = 4
              Example3: For a depth of 40, n = 40, N = (40 - 4) / 6 = 6
    :param k: Width of the network.
    :param dropout: Adds dropout if value is greater than 0.0
    :param verbose: Debug info to describe created WRN
    :return:
    """
    channel_axis = 1 if K.image_data_format() == "channels_first" else -1

    ip = Input(shape=input_dim)

    x = initial_conv(ip)
    nb_conv = 4

    x = expand_conv(x, 16, k)
    nb_conv += 2

    for i in range(N - 1):
        x = conv1_block(x, k, dropout)
        nb_conv += 2

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)

    x = expand_conv(x, 32, k, strides=(2, 2))
    nb_conv += 2

    for i in range(N - 1):
        x = conv2_block(x, k, dropout)
        nb_conv += 2

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)

    x = expand_conv(x, 64, k, strides=(2, 2))
    nb_conv += 2

    for i in range(N - 1):
        x = conv3_block(x, k, dropout)
        nb_conv += 2

    x = BatchNormalization(axis=channel_axis, momentum=0.1,
                           epsilon=1e-5, gamma_initializer='uniform')(x)
    x = Activation('relu')(x)

    x = AveragePooling2D((8, 8))(x)
    x = Flatten()(x)

    x = Dense(nb_classes, kernel_regularizer=l2(
        weight_decay), activation='softmax')(x)

    model = Model(ip, x)

    if verbose:
        print("Wide Residual Network-%d-%d created." % (nb_conv, k))
    return model


if __name__ == "__main__":
    from keras.utils import plot_model
    from keras.layers import Input
    from keras.models import Model

    init = (32, 32, 3)

    wrn_28_10 = create_wide_residual_network(
        init, nb_classes=10, N=2, k=2, dropout=0.0)

    wrn_28_10.summary()

    plot_model(wrn_28_10, "WRN-16-2.png",
               show_shapes=True, show_layer_names=True)
