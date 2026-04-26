# ⚡ NumPy for Machine Learning

## 🖥️ Why NumPy?
- Python is the language, but pure Python lists are slow for large-scale data.

- NumPy (Numerical Python) provides fast, efficient arrays written in C.

- Operations on millions of numbers take milliseconds instead of minutes.

- Every AI framework (PyTorch, TensorFlow, scikit-learn, Pandas) relies on NumPy arrays.


      import numpy as np

      # Python list vs NumPy speed demo
        import time

      py_list = list(range(1000000))
      np_array = np.arange(1000000)

      # Python list doubling
      start = time.time()
      py_list = [x*2 for x in py_list]
      print("Python list time:", time.time()-start)

      # NumPy array doubling
      start = time.time()
      np_array = np_array*2
      print("NumPy array time:", time.time()-start)




## 🚀 Speed Test
- Doubling 1 million numbers:

- Python list → ~`0.0812s`

- NumPy array → ~`0.0018s`

- ~45× faster because NumPy skips Python loops and uses optimized C operations.





## Creating Arrays📦
- From lists: `np.array([88, 92, 76, 85, 90])` → 1D array.

- 2D arrays (matrices): `np.array([[1,2,3],[4,5,6],[7,8,9]])`.

- Attributes:

`.shape` → dimensions.

`.dtype` → data type of elements.


      # 1D array
      scores = np.array([88, 92, 76, 85, 90])

      # 2D array (matrix)
      matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])

      print("Shape:", matrix.shape)
      print("Data type:", matrix.dtype)





## 🏗️ Array Initializers
- `np.zeros((3,3))` → all zeros.

- `np.ones((2,4))` → all ones.

- `np.full((2,3),7)` → filled with 7.

- `np.eye(3)` → identity matrix.

- Useful for creating test data quickly.

- Identity and diagonal matrices are critical in linear algebra.

      zeros = np.zeros((3,3))
      ones = np.ones((2,4))
      full = np.full((2,3),7)
      identity = np.eye(3)

      print(zeros)
      print(identity)




## 🎲 Random Arrays
- `np.random.rand(3,3)` → random floats between 0–1.

- `np.random.randint(1,7,size=10)` → random integers (like dice rolls).

- `np.random.randn(5)` → normal distribution (bell curve).

- `np.random.seed(42)` → reproducibility of random numbers.

- Random numbers are essential for ML (weights initialization, sampling).

- `randn` generates values from a normal distribution (mean=0, std=1).


      rand_floats = np.random.rand(3,3)
      rand_ints = np.random.randint(1,7,size=10)  # dice rolls
      rand_normal = np.random.randn(5)

      np.random.seed(42)  # reproducibility
      print(rand_floats)




## ➕ Vectorized Math
- Operations apply to all elements without loops.

- Example: scores + 5 adds 5 to every element.

- Supported operators: `+, -, *, /, **.`

      scores = np.array([88, 92, 76, 85, 90])

      print(scores + 5)   # add 5 to all
      print(scores * 2)   # double all
      print(scores / 100) # normalize




## 📊 Built-in Statistics
- `.mean()` → average.

- `.std()` → standard deviation.

- `.max() / .min()` → highest and lowest values.

- `.sum()` → total.

- `np.argmax() / np.argmin()` → index of max/min.

- `np.sort()` → sorted array.

      print("Mean:", scores.mean())
      print("Std Dev:", scores.std())
      print("Max:", scores.max())
      print("Min:", scores.min())
      print("Sum:", scores.sum())
      print("Index of Max:", np.argmax(scores))
      print("Sorted:", np.sort(scores))



## 📡 Broadcasting

- Operates on arrays of different shapes.

- Example: scores / 100 normalizes values between 0–1.

- Example: `scores - scores.mean()` subtracts the average from each element.




      scores = np.array([88, 92, 76, 85, 90])

      normalized = scores / 100
      centered = scores - scores.mean()

      print("Normalized:", normalized)
      print("Centered:", centered)




## 🔢 Indexing & Slicing
- Access elements by `[row, column]`.

- `matrix[1,:]` → entire row.

- `matrix[:,1]` → entire column.

- Slicing: `matrix[:2,1:]` → sub-matrix.

- Reverse array: `scores[::-1]`.




      matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])

      print(matrix[1,:])   # second row
      print(matrix[:,1])   # second column
      print(matrix[:2,1:]) # sub-matrix
      print(scores[::-1])  # reverse



 ## 🔄 Reshape & Flatten
- `.flatten()` → convert to 1D.

- `.reshape()` → change dimensions while keeping data.

- Example: `(3,3) → (9,) or (1,9)`.

- -1 lets NumPy auto-calculate dimensions.


      matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])

      flat = matrix.flatten()
      reshaped = matrix.reshape(1,9)
      auto = matrix.reshape(-1,3)

      print(flat)
      print(reshaped)
      print(auto)


## 🖼️ Arrays in ML
- Images: `(28,28)` grayscale arrays for handwritten digits.

- Color images: `(height,width,3)` for RGB channels.

- Audio: `(samples,)` amplitude over time.

- Text: `(words,features)` embeddings.

- Video: `(frames,h,w,3)` stack of images.

- Time series: `(days,)` for stock prices.

      # Example: grayscale image (28x28)
      image = np.random.randint(0,255,(28,28))

      # Example: RGB image (height,width,3)
      color_image = np.random.randint(0,255,(64,64,3))

      # Example: audio waveform
      audio = np.random.randn(44100)  # 1 second of samples

      print(image.shape, color_image.shape, audio.shape)



## 🎨 Pixel Art Lab
- Build a `16×16` NumPy array where each cell is a pixel.

- Values:  `0 = black, 1 = white`.

- Use indexing, slicing, and reshaping to draw shapes.

- Display with `matplotlib.pyplot.imshow()`.


      import matplotlib.pyplot as plt

      # 16x16 pixel art
      canvas = np.zeros((16,16))

      # Draw a white square in the center
      canvas[6:10,6:10] = 1

      plt.imshow(canvas, cmap="gray")
      plt.show()



## 📌 Summary
- NumPy arrays are the foundation of ML data.

- Operations are fast, vectorized, and memory-efficient.

- Covers creation, randomization, math, stats, broadcasting, indexing, slicing, reshaping.

- Real-world ML data (images, audio, text, video) are all arrays.

- Pixel art lab connects theory to practice.

- Advanced tools: stacking, splitting, linear algebra, boolean indexing.

- NumPy is the gateway to ML coding.
