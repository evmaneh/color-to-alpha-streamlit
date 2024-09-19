import numpy as np

def interpolate(x, interpolation=None):
    if interpolation == 'power':
        return x**2
    elif interpolation == 'root':
        return np.sqrt(x)
    elif interpolation == 'smooth':
        return (np.sin(np.pi/2*x))**2
    elif interpolation == 'inverse-sin':
        return np.arcsin(2*x-1)/np.pi + 0.5
    else:
        return x

def rgb_distance(pixels: np.array, color: np.array, shape='cube'):
    '''
    Calculate distance between colors
    If shape is 'cube', use maximum orthogonal distance
    If shape is 'sphere', use Euclidean distance
    '''
    pixels = pixels[:,:,:3]

    if shape == 'cube':
        return np.amax(abs(pixels - color), axis=2)
    elif shape == 'sphere':
        return np.linalg.norm(pixels - color, axis=2)

def color_to_alpha(pixels, color, transparency_threshold, opacity_threshold, shape='cube', interpolation=None):
    '''
    Apply the GIMP color to alpha algorithm
    Pixels within transparency_threshold become transparent
    Pixels within opacity_threshold remain opaque
    Pixels between thresholds transition smoothly
    '''
    color = np.array(color)

    if pixels.ndim == 2:
        pixels = np.stack([pixels] * 3, axis=-1)

    pixels = pixels[:,:,:3]
    new_pixels = np.copy(pixels)
    new_pixels = np.append(new_pixels, np.zeros((new_pixels.shape[0], new_pixels.shape[1], 1), dtype=np.uint8), axis=2)

    distances = rgb_distance(pixels, color, shape=shape)

    transparency_mask = distances <= transparency_threshold
    opacity_mask = distances >= opacity_threshold

    threshold_difference = opacity_threshold - transparency_threshold
    alpha = (distances - transparency_threshold) / threshold_difference
    alpha = np.clip(alpha, 0, 1)

    alpha = interpolate(alpha, interpolation=interpolation)

    proportion_to_opacity = distances / opacity_threshold
    extrapolated_colors = (pixels - color) / proportion_to_opacity[:, :, np.newaxis] + color
    
    extrapolated_colors = np.nan_to_num(extrapolated_colors, nan=0)
    extrapolated_colors = np.clip(np.around(extrapolated_colors), 0, 255).astype(np.uint8)

    new_pixels[~transparency_mask & ~opacity_mask, :3] = extrapolated_colors[~transparency_mask & ~opacity_mask]
    new_pixels[:, :, 3] = alpha * 255
    
    return new_pixels
