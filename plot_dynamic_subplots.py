def plot_dynamic_subplots(sdata, crop=None, save_png=False):

    shape_titles = list(sdata.shapes.keys())
    shape_titles.remove("sopa_patches")

    num_plots = len(shape_titles)
    num_cols = round(math.sqrt(num_plots))
    num_rows = num_cols + 1
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6 * num_rows))
    fig.patch.set_facecolor('black')
    
    axes = axes.flatten() if num_plots > 1 else [axes]

    if crop is not None:
        cropped_sdata = sdata.query.bounding_box(
            axes=["x", "y"],
            min_coordinate=[crop[0], crop[1]],
            max_coordinate=[crop[2], crop[3]],
            target_coordinate_system='pixels')

    for ax, title in zip(axes, shape_titles):
        ax.set_facecolor('black')
        ax.title.set_color('white')
        if crop is not None:
            try:
                cropped_sdata.pl.render_images(element="991_subset", alpha=0.85, channel=["DAPI_bg", "DAPI_1"], palette=['white', 'white']).pl.show(ax=ax, title=title)
                cropped_sdata.pl.render_shapes(element=title, fill_alpha=0.0, outline=True, outline_width=1.5, outline_color="yellow", outline_alpha=0.32).pl.show(ax=ax, title=title)
            except:
                print(f"Could not render {title} in the specified crop area.")
        else:
            try:
                sdata.pl.render_images(element="991_subset", alpha=0.85, channel=["DAPI_bg", "DAPI_1"], palette=['white', 'white']).pl.show(ax=ax, title=title)
                sdata.pl.render_shapes(element=title, fill_alpha=0.0, outline=True, outline_width=1.5, outline_color="yellow", outline_alpha=0.32).pl.show(ax=ax, title=title)
            except:
                print(f"Could not render {title} in the specified")

    # Hide any unused subplots
    for ax in axes[len(shape_titles):]:
        ax.set_visible(False)

    plt.tight_layout()
    if save_png:
        plt.savefig(save_png, dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()