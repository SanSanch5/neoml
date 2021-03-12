""" Copyright (c) 2017-2021 ABBYY Production LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
--------------------------------------------------------------------------------------------------------------
"""

import numpy
from scipy.sparse import csr_matrix
import neoml.PythonWrapper as PythonWrapper

class FirstCome(PythonWrapper.FirstCome) :
    """FirstCome clustering.
    Parameters
    ----------
    distance : {'euclid', 'machalanobis', 'cosine'}, default='euclid' the distance function.

    min_vector_count : the smallest number of vectors in a cluster to consider that the variance is valid.

    default_variance : the default variance (for when the number of vectors is smaller than min_vector_count).

    threshold : the distance threshold for creating a new cluster.

    min_cluster_size_ratio : the minimum ratio of elements in a cluster (relative to the total number of vectors).

    min_cluster_size_ratio : the minimum ratio of elements in a cluster (relative to the total number of vectors).

    max_cluster_count : the maximum number of clusters to prevent algorithm divergence in case of great differences in data.
    """

    def __init__(self, min_vector_count=4, default_variance=1.0, threshold=0.0, min_cluster_size_ratio=0.05, max_cluster_count=100, distance='euclid'):

        if distance != 'euclid' and distance != 'machalanobis' and distance != 'cosine':
            raise ValueError('The `distance` must be one of {`euclid`, `machalanobis`, `cosine`}.')
        if max_cluster_count <= 0:
            raise ValueError('The `max_cluster_count` must be > 0.')
        if min_cluster_size_ratio > 1 or min_cluster_size_ratio < 0:
            raise ValueError('The `min_cluster_size_ratio` must be in [0, 1].')

        super().__init__(distance, int(min_vector_count), float(default_variance), float(threshold), float(min_cluster_size_ratio), int(max_cluster_count))

    def clusterize(self, X, weight=None):
        """.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.
        weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : object
        """
        x = csr_matrix( X, dtype=numpy.float32 )

        if weight is None:
            weight = numpy.ones(x.size, numpy.float32)
        else:
            weight = numpy.array(weight, dtype=numpy.float32, copy=False)
            if numpy.any(weight < 0):
                raise ValueError('All `weight` elements must be >= 0.')

        return super().clusterize(x.indices, x.data, x.indptr, int(x.shape[1]), weight)

#-------------------------------------------------------------------------------------------------------------


class Hierarchical(PythonWrapper.Hierarchical) :
    """Hierarchical clustering.
    Parameters
    ----------
    distance : {'euclid', 'machalanobis', 'cosine'}, default='euclid' the distance function.

    max_cluster_distance : the maximum distance between two clusters that still may be merged.

    min_cluster_count : the minimum number of clusters in the result.
    """

    def __init__(self, max_cluster_distance, min_cluster_count, distance='euclid'):

        if distance != 'euclid' and distance != 'machalanobis' and distance != 'cosine':
            raise ValueError('The `distance` must be one of {`euclid`, `machalanobis`, `cosine`}.')
        if min_cluster_count <= 0:
            raise ValueError('The `min_cluster_count` must be > 0.')

        super().__init__(distance, int(max_cluster_distance), int(min_cluster_count))

    def clusterize(self, X, weight=None):
        """.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.
        weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : object
        """
        x = csr_matrix( X, dtype=numpy.float32 )

        if weight is None:
            weight = numpy.ones(x.size, numpy.float32)
        else:
            weight = numpy.array(weight, dtype=numpy.float32, copy=False)
            if numpy.any(weight < 0):
                raise ValueError('All `weight` elements must be >= 0.')

        return super().clusterize(x.indices, x.data, x.indptr, int(x.shape[1]), weight)

#-------------------------------------------------------------------------------------------------------------


class IsoData(PythonWrapper.IsoData) :
    """IsoData clustering.
    Parameters
    ----------

    init_cluster_count : the number of initial clusters.
        The initial cluster centers are randomly selected from the input data.

    max_iteration_count : the maximum number of clusters.

    min_cluster_size : the minimum cluster size.

    max_iteration_count : the maximum number of algorithm iterations. 

    min_cluster_distance : the minimum distance between the clusters.
        Whenever two clusters are closer they are merged.

    max_cluster_diameter : the maximum cluster diameter.
        Whenever a cluster is larger it may be split.

    mean_diameter_coef : indicates how much the cluster diameter may exceed.
        The mean diameter across all the clusters. If a cluster diameter is larger than the mean diameter multiplied by this value it may be split.

    """

    def __init__(self, init_cluster_count, max_cluster_count, min_cluster_size, max_iteration_count, min_cluster_distance, max_cluster_diameter, mean_diameter_coef ):

        if max_iteration_count <= 0:
            raise ValueError('The `max_iteration_count` must be > 0.')
        if init_cluster_count <= 0:
            raise ValueError('The `init_cluster_count` must be > 0.')
        if min_cluster_size <= 0:
            raise ValueError('The `min_cluster_size` must be > 0.')

        super().__init__( int(init_cluster_count), int(max_cluster_count), int(min_cluster_size), int(max_iteration_count), float(min_cluster_distance), float(max_cluster_diameter), float(mean_diameter_coef) )

    def clusterize(self, X, weight=None):
        """.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.
        weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : object
        """
        x = csr_matrix( X, dtype=numpy.float32 )

        if weight is None:
            weight = numpy.ones(x.size, numpy.float32)
        else:
            weight = numpy.array(weight, dtype=numpy.float32, copy=False)
            if numpy.any(weight < 0):
                raise ValueError('All `weight` elements must be >= 0.')

        return super().clusterize(x.indices, x.data, x.indptr, int(x.shape[1]), weight)

#-------------------------------------------------------------------------------------------------------------


class KMeans(PythonWrapper.KMeans) :
    """K-Means clustering.
    Parameters
    ----------

    max_iteration_count :

    init_cluster_count :

    algo : {'elkan', 'lloyd'}, default='lloyd'

    init : {'k++', 'default'}, default='default'

    distance : {'euclid', 'machalanobis', 'cosine'}, default='euclid'

    """

    def __init__(self, max_iteration_count, init_cluster_count, algo='lloyd', init='default', distance='euclid'):
        if algo != 'elkan' and algo != 'lloyd':
            raise ValueError('The `algo` must be one of {`elkan`, `lloyd`}.')
        if init != 'k++' and init != 'default':
            raise ValueError('The `init` must be one of {`k++`, `default`}.')
        if distance != 'euclid' and distance != 'machalanobis' and distance != 'cosine':
            raise ValueError('The `distance` must be one of {`euclid`, `machalanobis`, `cosine`}.')
        if max_iteration_count <= 0:
            raise ValueError('The `max_iteration_count` must be > 0.')
        if init_cluster_count <= 0:
            raise ValueError('The `init_cluster_count` must be > 0.')

        super().__init__(algo, init, distance, int(max_iteration_count), int(init_cluster_count))

    def clusterize(self, X, weight=None):
        """.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.
        weight : array-like of shape (n_samples,), default=None
            Sample weights. If None, then samples are equally weighted.

        Returns
        -------
        self : object
        """
        x = csr_matrix(X, dtype=numpy.float32)

        if weight is None:
            weight = numpy.ones(x.size, numpy.float32)
        else:
            weight = numpy.array(weight, dtype=numpy.float32, copy=False)
            if numpy.any(weight < 0):
                raise ValueError('All `weight` elements must be >= 0.')

        return super().clusterize(x.indices, x.data, x.indptr, int(x.shape[1]), weight)
