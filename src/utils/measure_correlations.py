"""Function to compute gram matrices."""

import torch


def gram(x: torch.Tensor) -> torch.Tensor:
    """
    Calculates the gram matrix of a tensor

    Parameters
    ----------
    x : Tensor
        feature map as a Tensor of shape (batch_size, channels, height, width)

    Returns
    -------
    G : Tensor
        The Gram matrix associated to x, of shape (batch_size, channels, channels).

    """
    (bs, ch, h, w) = x.size()
    f = x.view(bs, ch, w * h)
    f_T = f.transpose(1, 2)
    G = f.bmm(f_T) / (ch * h * w)
    return G
