def format_size(bytes_val: int) -> str:
    if bytes_val < 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}" if unit != 'B' else f"{int(bytes_val)} B"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"
