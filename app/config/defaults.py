DEFAULT_SETTINGS = {
    "general": {
        "language": "auto",
        "theme": "System",
        "start_minimized": False,
        "confirm_replace": True,
        "check_updates": True
    },
    "processing": {
        "workers": 0,  # 0 means Auto
        "quality": 82,
        "output_format": "WEBP",
        "webp_mode": "lossy",
        "size_threshold_kb": 400,
        "threshold_enabled": True,
        "keep_original_if_larger": True,
        "strip_metadata": True,
        "enable_resize": False,
        "max_width": 2000,
        "max_height": 2000,
        "keep_aspect_ratio": True,
        "only_shrink": True,
        "output_mode": "folder",
        "output_folder": "",
        "preserve_folder_structure": True,
        "skip_already_target_format": False,
        "collision_strategy": "skip"  # skip, overwrite, rename
    },
    "backup": {
        "enabled": True,
        "strategy": "timestamped"  # suffix or timestamped
    },
    "imagemagick": {
        "auto_detect": True,
        "custom_path": ""
    }
}

PRESETS = {
    "Web Optimized": {
        "output_format": "WEBP",
        "quality": 82,
        "webp_mode": "lossy",
        "size_threshold_kb": 400,
        "threshold_enabled": True,
        "keep_original_if_larger": True,
        "strip_metadata": True,
        "enable_resize": False,
        "preserve_folder_structure": True
    },
    "WordPress Media": {
        "output_format": "WEBP",
        "quality": 80,
        "webp_mode": "lossy",
        "size_threshold_kb": 250,
        "threshold_enabled": True,
        "enable_resize": True,
        "max_width": 2560,
        "max_height": 2560,
        "only_shrink": True,
        "strip_metadata": True
    },
    "High Quality Archive": {
        "output_format": "WEBP",
        "quality": 92,
        "webp_mode": "lossy",
        "threshold_enabled": False,
        "strip_metadata": False,
        "enable_resize": False
    },
    "Maximum Compression": {
        "output_format": "AVIF",
        "quality": 65,
        "threshold_enabled": True,
        "size_threshold_kb": 100,
        "strip_metadata": True,
        "enable_resize": True,
        "max_width": 1920,
        "max_height": 1080
    }
}
