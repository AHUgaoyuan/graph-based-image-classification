structure = {
    'conv': [
        {
            'output_channels': 64,
            'weights': {'stddev': 5e-2, 'decay': 0.0},
            'biases': {'constant': 0.0},
            'fields': {'size': [5, 5], 'strides': [1, 1]},
            'max_pool': {'size': [3, 3], 'strides': [2, 2]},
        },
        {
            'output_channels': 64,
            'weights': {'stddev': 5e-2, 'decay': 0.0},
            'biases': {'constant': 0.1},
            'fields': {'size': [5, 5], 'strides': [1, 1]},
            'max_pool': {'size': [3, 3], 'strides': [2, 2]},
        },
    ],
    'local': [
        {
            'output_channels': 384,
            'weights': {'stddev': 0.04, 'decay': 0.004},
            'biases': {'constant': 0.1},
        },
        {
            'output_channels': 192,
            'weights': {'stddev': 0.04, 'decay': 0.004},
            'biases': {'constant': 0.1},
        },
    ],
    'softmax_linear': {
        'output_channels': 10,
        'weights': {'stddev': 1/192.0, 'decay': 0.0},
        'biases': {'constant': 0.0},
    },
}
