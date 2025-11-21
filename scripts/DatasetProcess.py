import os
import json
import numpy as np
from PIL import Image
import tifffile


def create_instance_dataset(jpg_dir, json_dir, npy_dir, tif_dir, txt_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to track instance appearances
    instance_appearances = {}

    # Process each JSON file
    for json_file in os.listdir(json_dir):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(json_dir, json_file)
        with open(json_path, "r") as f:
            data = json.load(f)

        # Get mask, color, and depth file names from JSON
        mask_file = data["mask_name"]
        save_file = mask_file[5:9]
        # print("1111111", mask_file[5:9])
        color_file = (
            os.path.splitext(mask_file)[0].replace("mask_", "frame_") + ".jpg"
        )  # Example color file inference
        depth_file = (
            os.path.splitext(mask_file)[0].replace("mask_", "frame_") + ".tif"
        )  # Example depth file inference
        pose_file = (
            os.path.splitext(mask_file)[0].replace("mask_", "frame_") + ".txt"
        )  # Example pose file inference

        # Process each instance in the "labels" section
        for label_key, label_data in data["labels"].items():
            instance_id = label_data["instance_id"]
            bbox = (
                label_data["x1"],
                label_data["y1"],
                label_data["x2"],
                label_data["y2"],
            )

            # Create directories for the instance
            instance_dir = os.path.join(output_dir, f"p{instance_id}", "input")
            color_dir = os.path.join(instance_dir, "color")
            depth_dir = os.path.join(instance_dir, "depth")
            mask_dir = os.path.join(instance_dir, "mask")
            pose_dir = os.path.join(instance_dir, "pose")
            os.makedirs(color_dir, exist_ok=True)
            os.makedirs(depth_dir, exist_ok=True)
            os.makedirs(mask_dir, exist_ok=True)
            os.makedirs(pose_dir, exist_ok=True)

            # Track instance appearance
            if instance_id not in instance_appearances:
                instance_appearances[instance_id] = 0

            # Generate frame name
            instance_appearances[instance_id] += 1
            frame_name = f"frame{instance_appearances[instance_id]}"

            # Save the mask as an 8-bit PNG
            mask_path = os.path.join(npy_dir, mask_file)
            mask_image = np.load(mask_path)
            instance_mask = (mask_image == instance_id).astype(
                np.uint8
            ) * 255  # Isolate instance mask
            # mask_output_path = os.path.join(mask_dir, f"{frame_name}.png")
            mask_output_path = os.path.join(mask_dir, f"{save_file}.png")
            Image.fromarray(instance_mask).save(mask_output_path)

            # Save the pose file
            pose_path = os.path.join(txt_dir, pose_file)
            # print(pose_path)
            if os.path.exists(pose_path):
                #   print(pose_path)
                # pose_output_path = os.path.join(pose_dir, f"{frame_name}.txt")
                pose_output_path = os.path.join(pose_dir, f"{save_file}.txt")

                with open(pose_path, "r") as pose_file_in, open(
                    pose_output_path, "w+"
                ) as pose_out:
                    pose_out.write(pose_file_in.read())

            # Save the color file as PNG
            color_path = os.path.join(jpg_dir, color_file)
            if os.path.exists(color_path):
                color_image = Image.open(color_path)
                # color_output_path = os.path.join(color_dir, f"{frame_name}.png")
                color_output_path = os.path.join(color_dir, f"{save_file}.png")

                color_image.save(color_output_path)

            # Save the depth file as .npy
            depth_path = os.path.join(tif_dir, depth_file)
            if os.path.exists(depth_path):
                depth_image = tifffile.imread(depth_path)
                # depth_output_path = os.path.join(depth_dir, f"{frame_name}.npy")
                depth_output_path = os.path.join(depth_dir, f"{save_file}.npy")

                np.save(depth_output_path, depth_image)

    print(f"Dataset created at {output_dir}")


# Paths for the input directories
jpg_dir = ""
json_dir = ""
npy_dir = ""
tif_dir = ""
txt_dir = ""

# Output directory for the dataset
output_dir = ""

# Create dataset
create_instance_dataset(jpg_dir, json_dir, npy_dir, tif_dir, txt_dir, output_dir)
