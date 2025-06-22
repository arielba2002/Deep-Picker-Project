#!/usr/bin/env python3
"""
Simple test script to verify TensorFlow installation in Docker container.
This will help debug CPU instruction compatibility issues.
"""

print("=== TensorFlow Import Test ===")

try:
    print("1. Testing basic imports...")
    import sys
    print(f"   Python version: {sys.version}")
    
    import numpy as np
    print(f"   NumPy version: {np.__version__}")
    
    import pandas as pd
    print(f"   Pandas version: {pd.__version__}")
    
    print("2. Testing TensorFlow import...")
    import tensorflow as tf
    print(f"   TensorFlow version: {tf.__version__}")
    
    print("3. Testing TensorFlow basic operations...")
    # Test basic tensor operations
    a = tf.constant([1, 2, 3])
    b = tf.constant([4, 5, 6])
    c = tf.add(a, b)
    print(f"   Basic operation result: {c.numpy()}")
    
    print("4. Testing Keras import...")
    from tensorflow.keras.models import load_model
    from tensorflow.keras.layers import Lambda
    print("   Keras imports successful")
    
    print("5. Testing custom functions...")
    def mean_pool(t):
        return tf.reduce_mean(t, axis=1)
    
    def max_pool(t):
        return tf.reduce_max(t, axis=1)
    
    # Test the functions
    test_tensor = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    mean_result = mean_pool(test_tensor)
    max_result = max_pool(test_tensor)
    print(f"   Mean pool result: {mean_result.numpy()}")
    print(f"   Max pool result: {max_result.numpy()}")
    
    print("6. Testing other ML libraries...")
    import sklearn
    print(f"   Scikit-learn version: {sklearn.__version__}")
    
    import matplotlib
    print(f"   Matplotlib version: {matplotlib.__version__}")
    
    import h5py
    print(f"   H5py version: {h5py.__version__}")
    
    print("\n✅ ALL TESTS PASSED! TensorFlow is working correctly.")
    
except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ RUNTIME ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 