# Machine Learning
This sections include multiple jupyter notebooks used to explore the data, train models, and understand qualities of the models. A lot of experimentation with different architectures was done in an attempt to improve the performance of the system. Much of that experimentation is included in the notebooks in this section.

## Architecture Development
The first implementation consisted of a seperately trained linear autoencoder, reducing the 63 point dimensions to a vector of 9 numbers. This autoencoder was then used to train a two layer LSTM network resulting in a model with ~55k parameters.

Then a fully connected architecture was explored that trained the two LSTM layers in conjunction with several fully connected layers to directly produce the 63 output parameters.

This architecture was then dramatically expanded into 3 LSTM layers and a much larger FC network with added dropout and batch normalization.

This progression is explored in the `primary_model_pipeline.ipynb` and `primary_model_pipeline_large_dataset.ipynb` notebooks.

The other notebooks explore the final architecture with various datasets including a very large datasets with several hours of training data, and datasets with only very specific data, such as a single finger movement, etc.

## Network Architecture
The current best architecture is described below. This network has ~1.4M parameters. A network of this size showed the best performance but the high dropout rates indicate that network could be compressed or pruned.
```python
model_fc = tf.keras.models.Sequential()
model_fc.add(LSTM(256, return_sequences=True, input_shape=(seq_length, 8)))
model_fc.add(Dropout(0.5))
model_fc.add(LSTM(256, return_sequences=True))
model_fc.add(Dropout(0.5))
model_fc.add(LSTM(128))
model_fc.add(BatchNormalization())
model_fc.add(Dense(512, input_dim=128))
model_fc.add(Activation('relu'))
model_fc.add(BatchNormalization())
model_fc.add(Dropout(0.5))
model_fc.add(Dense(512, input_dim=512))
model_fc.add(Activation('relu'))
model_fc.add(BatchNormalization())
model_fc.add(Dropout(0.5))
model_fc.add(Dense(256, input_dim=512))
model_fc.add(Activation('relu'))
model_fc.add(Dropout(0.3))
model_fc.add(Dense(63, input_dim=64))

model_fc.compile(optimizer='Adam', loss='mse')
```

The 'Adam' optimizer is used with Mean Squared Error.