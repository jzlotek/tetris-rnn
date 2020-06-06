import tensorflow.keras as ks
ls = ks.layers


def init_model(debug=False):
    batch_size = 32
    board_input = ls.Input(shape=(batch_size, 20, 10))
    aux_input = ls.Input(shape=(batch_size, 5,))

    # Board state
    x = ls.Conv2D(
        filters=24,
        kernel_size=4,
        padding="same",
        activation="sigmoid",
    )(board_input)
    x = ls.MaxPooling2D(
        pool_size=(2, 2),
        strides=1,
    )(x)
    x = ls.Flatten()(x)
    x = ks.Model(inputs=board_input, outputs=x)

    # Next piece + input info
    y = ls.Dense(
        units=18,
    )(aux_input)
    y = ls.Flatten()(y)
    y = ks.Model(inputs=aux_input, outputs=y)

    # All input combined
    combined = ls.concatenate([x.output, y.output])

    # Combined model
    z = ls.Reshape(
        target_shape=(8, combined.shape[1]),
    )(combined)
    z = ls.LSTM(
        units=64,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
    )(z)
    z = ls.Reshape(
        target_shape=(4, z.shape[1]),
    )(z)
    z = ls.LSTM(
        units=32,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
    )(z)
    z = ls.Dense(
        units=16,
        activation="relu",
    )(z)
    z = ls.Dense(
        units=4,
        activation="sigmoid",
    )(z)

    model = ks.Model(inputs=[x.input, y.input], outputs=z)

    if debug:
        model.summary()
        ks.utils.plot_model(model, to_file="./model.png")

    return model


def main():
    _ = init_model(debug=True)


if __name__ == "__main__":
    main()
