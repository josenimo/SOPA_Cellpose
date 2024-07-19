for i, (flow_threshold, cellprob_threshold) in enumerate(zip(flow_thresholds, cellprob_thresholds)):
    method = sopa.segmentation.methods.cellpose_patch(diameter=25, channels=channels, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, model_type="nuclei")
    segmentation = sopa.segmentation.StainingSegmentation(sdata, method, channels, min_area=300)
    cellpose_temp_dir = f"tuto_{i}.zarr/.sopa_cache/cellpose"
    segmentation.write_patches_cells(cellpose_temp_dir)
    
    cells = sopa.segmentation.StainingSegmentation.read_patches_cells(cellpose_temp_dir)
    cells = sopa.segmentation.shapes.solve_conflicts(cells)
    sopa.segmentation.StainingSegmentation.add_shapes(sdata, cells, image_key="991_subset", shapes_key=f"cellpose_boundaries_FT{flow_threshold}_CT{cellprob_threshold}")