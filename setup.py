import setuptools


with open('README.md', 'r') as f:
  long_description = f.read()

setuptools.setup(
  name='invisible-watermark-gpu',
  version='0.1.0',
  author='Will Drevo',
  author_email='will.drevo@gmail.com',
  description='GPU adaptation for the library for creating and decoding invisible image watermarks',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/worldveil/invisible-watermark',
  packages=setuptools.find_packages(),
  install_requires=[
      'opencv-python>=4.1.0.25',
      'torch>=2.0.0',
      'Pillow>=6.0.0',
      'PyWavelets>=1.1.1',
      'numpy>=1.17.0',
      # 'pycudwt==1.0.2',  # this is our old dependency, we replace with one below to compile for multiple GPUs
      'pycudwt @ git+https://github.com/worldveil/pypwt@9f062ebdee4ab97d9df783c3521524fe5d3281dd#egg=pycudwt',
      'pytest',
  ],
  scripts=['invisible-watermark'],
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: POSIX :: Linux',
  ],
  # Python 3.6 tested in Ubuntu 18.04 LTS.
  python_requires='>=3.6',
  include_package_data=True,
)
