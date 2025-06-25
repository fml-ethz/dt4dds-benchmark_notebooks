import dt4dds_benchmark

POOL_CODECS = [

    # 
    # aeon codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.DNAAeon.max_coderate_pool(), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "aeon_max",
        'index': "AAA",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNAAeon.high_coderate_pool(), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "aeon_high",
        'index': "ACC",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNAAeon.medium_coderate_pool(), 
        'input': dt4dds_benchmark.inputs.pool_17kB, 
        'name': "aeon_medium",
        'index': "AGG",
    },

    # 
    # fountain codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.DNAFountain.max_coderate_pool(dt4dds_benchmark.inputs.pool_19kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "fountain_max",
        'index': "ATT",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNAFountain.high_coderate_pool(dt4dds_benchmark.inputs.pool_19kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "fountain_high",
        'index': "CAC",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNAFountain.medium_coderate_pool(dt4dds_benchmark.inputs.pool_17kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_17kB, 
        'name': "fountain_medium",
        'index': "CCA",
    },

    # 
    # rs codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.DNARS.max_coderate_pool(dt4dds_benchmark.inputs.pool_19kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "rs_max",
        'index': "CGT",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNARS.high_coderate_pool(dt4dds_benchmark.inputs.pool_19kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "rs_high",
        'index': "CTG",
    },
    {
        'codec': dt4dds_benchmark.codecs.DNARS.medium_coderate_pool(dt4dds_benchmark.inputs.pool_17kB.stat().st_size), 
        'input': dt4dds_benchmark.inputs.pool_17kB, 
        'name': "rs_medium",
        'index': "GAG",
    },

    # 
    # hedges codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.HEDGES.medium_coderate_pool(), 
        'input': dt4dds_benchmark.inputs.pool_17kB, 
        'name': "hedges",
        'index': "GTC",
    },

    # 
    # goldman codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.Goldman.default(), 
        'input': dt4dds_benchmark.inputs.pool_5kB, 
        'name': "goldman",
        'index': "TAT",
    },

    # 
    # yin-yang codec
    # 
    {
        'codec': dt4dds_benchmark.codecs.YinYang.default_pool(), 
        'input': dt4dds_benchmark.inputs.pool_19kB, 
        'name': "yinyang",
        'index': "TCG",
    },
]