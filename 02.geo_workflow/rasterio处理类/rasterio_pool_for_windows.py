# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 19:33:33 2020

@author: YeHui
"""
with rasterio.Env():

    with rasterio.open(infile) as src:

        # Create a destination dataset based on source params. The
        # destination will be tiled, and we'll process the tiles
        # concurrently.
        profile = src.profile
        profile.update(blockxsize=128, blockysize=128, tiled=True)

        with rasterio.open(outfile, "w", **profile) as dst:

            # Materialize a list of destination block windows
            # that we will use in several statements below.
            windows = [window for ij, window in dst.block_windows()]

            # This generator comprehension gives us raster data
            # arrays for each window. Later we will zip a mapping
            # of it with the windows list to get (window, result)
            # pairs.
            data_gen = (src.read(window=window) for window in windows)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_workers
            ) as executor:

                # We map the compute() function over the raster
                # data generator, zip the resulting iterator with
                # the windows list, and as pairs come back we
                # write data to the destination dataset.
                for window, result in zip(
                    windows, executor.map(compute, data_gen)
                ):
                    dst.write(result, window=window)

