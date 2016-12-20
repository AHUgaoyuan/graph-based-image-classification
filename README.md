# A TensorFlow implementation of Graph-based Image Classification

[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Requirements Status][requirements-image]][requirements-url]
[![Code Climate][code-climate-image]][code-climate-url]
[![Code Climate Issues][code-climate-issues-image]][code-climate-issues-url]

This is a TensorFlow implementation based on my "[Graph-based Image
Classification](https://github.com/rusty1s/deep-learning/tree/master/thesis)"
master thesis.

## Requirements

Project is tested on Python 2.7, 3.4 and 3.5.

[TensorFlow](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html#pip-installation),
[nauty](http://pallini.di.uniroma1.it/) and its python wrapper
[pynauty](https://web.cs.dal.ca/~peter/software/pynauty/html/install.html)
need to be installed before running the script.

To install the additional required python packages, run:

```bash
pip install -r requirements.txt
```

### Tested Versions

* **TensorFlow**: 0.12.0
* **nauty**: 26r7
* **pynauty**: 0.6.0
* **OpenCV**: 3.1.0

## Miniconda

If you have [Miniconda
installed](http://conda.pydata.org/docs/install/quick.html#miniconda-quick-install-requirements),
you can simply run

```bash
./bin/install.sh graph
```

to install all dependencies (including TensorFlow and nauty/pynauty) in a new
conda environment with name `"graph"`.

For configuration and usage of the install script, run:

```bash
./bin/install.sh --help
```

To install Miniconda, run

```bash
./bin/conda.sh
```

and add `~/.miniconda/bin` to your path.

## Running tests

Install the test requirements:

```bash
pip install -r requirements_test.txt
```

Run the test suite:

```bash
./bin/test.sh
```

## ToDos

* cifar labels should hold an array of 10
* nextbatch method for cifar?
* Normalization no use of weights?

[build-image]: https://travis-ci.org/rusty1s/graph-based-image-classification.svg?branch=master
[build-url]: https://travis-ci.org/rusty1s/graph-based-image-classification
[coverage-image]: https://img.shields.io/codecov/c/github/rusty1s/graph-based-image-classification.svg
[coverage-url]: https://codecov.io/github/rusty1s/graph-based-image-classification?branch=master
[requirements-image]: https://requires.io/github/rusty1s/graph-based-image-classification/requirements.svg?branch=master
[requirements-url]: https://requires.io/github/rusty1s/graph-based-image-classification/requirements/?branch=master
[code-climate-image]: https://codeclimate.com/github/rusty1s/graph-based-image-classification/badges/gpa.svg
[code-climate-url]: https://codeclimate.com/github/rusty1s/graph-based-image-classification
[code-climate-issues-image]: https://codeclimate.com/github/rusty1s/graph-based-image-classification/badges/issue_count.svg
[code-climate-issues-url]: https://codeclimate.com/github/rusty1s/graph-based-image-classification/issues
