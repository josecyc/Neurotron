# Machine Learning
This sections include multiple jupyter notebooks used to explore the data, train models, and understand qualities of the models. A lot of experimentation with different architectures was done in an attempt to improve the performance of the system. Much of that experimentation is included in the notebooks in this section.

## Architecture Development
### Autoencoder + LSTM
The first implementation consisted of a seperately trained linear autoencoder, reducing the 63 point dimensions to a vector of 9 numbers. This autoencoder was then used to train a two layer LSTM network resulting in a model with ~55k parameters.

Then a fully connected architecture was explored that trained the two LSTM layers in conjunction with several fully connected layers to directly produce the 63 output parameters.

### LSTM + FC
This architecture was then dramatically expanded into 3 LSTM layers and a much larger FC network with added dropout and batch normalization.

This progression is explored in the `primary_model_pipeline.ipynb` and `primary_model_pipeline_large_dataset.ipynb` notebooks.

The other notebooks explore the final architecture with various datasets including a very large datasets with several hours of training data, and datasets with only very specific data, such as a single finger movement, etc.

### CONV + LSTM
In the second phase of the project, in the spirit of exploring and optimizing more of the models architecture, we took a series of different approaches to understand what kind of influence might this have on the mapping.

The CONV + LSTM approach constist of transforming signal sequences to spectrograms, we then perform feature extraction with convolutional layers, the extracted features corresponding to every time-step are then given as input to the LSTMs. 

This is an expensive approach, where all our data gets transformed to overlapped sequences images, which turns a 100 MB dataset into a 7 GB dataset, it also adds Xms to the preprocessing so training 
this can be appreciated in `CNN_LSTM_pipeline.ipynb` 

### CONV2D_LSTM
This implementation includes a convolutional layer across every operation of the LSTM. The results of this were, very similar to a simple CONV + LSTM, without much difference.

### Attention
We added an attention module to the LSTM, what this does is multiply elementwise the output result of the LSTM, typically enabling to represent dependencies between the time-steps in a better way. The hypothesis in our case is that, there might be sparse dependencies for particular hand movements or positions that could be better represented with an attention layer. So far we haven't find evidence of an improvement in performance. The experiments of this approach are available in the `attention_model_pipeline.ipynb` notebook.

### Performance comparison
<table class="tg">
  <tr>
    <th class="tg-c3ow">method</th>
    <th class="tg-0pky">val-loss [mm]<br></th>
  </tr>
  <tr>
    <td class="tg-0pky">Dense (217k)</td>
    <td class="tg-0pky">23</td>
  </tr>
  <tr>
    <td class="tg-0pky">LSTM + AE (55k)</td>
    <td class="tg-0pky">20.3</td>
  </tr>
  <tr>
    <td class="tg-0pky">LSTM + AE (3.6k)</td>
    <td class="tg-0pky">23</td>
  </tr>
  <tr>
    <td class="tg-0pky">LSTM + FC (69k)</td>
    <td class="tg-0pky">20.5</td>
  </tr>
  <tr>
    <td class="tg-0pky">LSTM + FC (1.5M)</td>
    <td class="tg-0pky">21.2<br></td>
  </tr>
  <tr>
    <td class="tg-0pky">CNN + LSTM<br></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">Conv2D_LSTM</td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">LSTM + Attention (80k shared vector .3 dropout)</td>
    <td class="tg-0pky">20.7<br></td>
  </tr>
</table>

There seems to be no representative difference between most models, except when they become too large , too small or don't include LSTMs. 

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
