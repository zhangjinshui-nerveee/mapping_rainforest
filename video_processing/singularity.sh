video_file="P0740368"
images_dir="$HOME/rainforest/${video_file}_trunc/"
name=`basename $images_dir`
output_dir="$HOME/rainforest/outputs/${video_file}_trunc"
mkdir -p $output_dir
mkdir -p $output_dir/code/images

singularity run --nv --bind $images_dir:$output_dir/code/images, \
--writable-tmpfs odm_gpu.sif \
--orthophoto-png --mesh-octree-depth 12 --ignore-gsd --dtm \
--smrf-threshold 0.4 --smrf-window 24 --dsm --pc-csv --pc-las --orthophoto-kmz \
--ignore-gsd  --matcher-type flann --feature-quality ultra --max-concurrency 16 \
--use-hybrid-bundle-adjustment --build-overviews --time --min-num-features 10000 \
--project-path $output_dir --geo geo_${video_file}.txt

