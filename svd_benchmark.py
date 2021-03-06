# Fastest way to compute eigenvectors for 4k matrix?
#
# Xeon V3 benchmarks:
# n=4096 eigs  min: 27758.34, median: 28883.69
# n=4096 gesdd min: 7241.70, median: 8477.95
# n=4096 gesvd min=20487.48, median: 22057.64,
#
# Xeon V4:
# n=4096 gesdd min: 5586.02, median: 6032.16
#
#
# i7-5820K CPU @ 3.30GHz
# n=4096 gesdd 7288.02, median: 7397.23, mean: 7478.78
# n=4096 inv 520 msec


from scipy import linalg  # for svd
import numpy as np
import time
import sys

methods = ['gesdd', 'gesvd', 'eigh']

if len(sys.argv)<2:
  method = methods[0]
else:
  method = sys.argv[1]

assert method in methods

n=4096
x = np.random.randn(n*n).reshape((n,n)).astype(dtype=np.float32)
x = x @ x.T
start_time = time.time()
times = []

print("n=%d %s "%(n, method))
for i in range(9):
  if method == 'gesdd':
    result = linalg.svd(x)
  elif method == 'gesvd':
    result = linalg.svd(x, lapack_driver='gesvd')
  elif method == 'eigh':
    result = linalg.eigh(x)
  else:
    assert False
  new_time = time.time()
  elapsed_time = 1000*(new_time - start_time)
  print("%.2f msec" %(elapsed_time))
  start_time = new_time
  times.append(elapsed_time)

print("Times: min: %.2f, median: %.2f, mean: %.2f"%(np.min(times), np.median(times), np.mean(times)))


# Other timings
# n=1000 Times: min: 126.04, median: 132.48
# n=2000 Times: min: 573.03, median: 621.49
# n=4096 Times: min: 5586.02, median: 6032.16
