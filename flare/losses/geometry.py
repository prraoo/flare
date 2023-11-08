# Code: https://github.com/fraunhoferhhi/neural-deferred-shading/tree/main
# Modified/Adapted by: Shrisha Bharadwaj

import torch

from flare.core import Mesh

def laplacian_loss(mesh: Mesh):
    """ Compute the Laplacian term as the mean squared Euclidean norm of the differential coordinates.

    Args:
        mesh (Mesh): Mesh used to build the differential coordinates.
    """

    L = mesh.laplacian
    V = mesh.vertices
    
    loss = L.mm(V)
    loss = loss.norm(dim=1)**2
    
    return loss.mean()

def normal_consistency_loss(mesh: Mesh):
    """ Compute the normal consistency term as the cosine similarity between neighboring face normals.

    Args:
        mesh (Mesh): Mesh with face normals.
    """

    loss = 1 - torch.cosine_similarity(mesh.face_normals[mesh.connected_faces[:, 0]], mesh.face_normals[mesh.connected_faces[:, 1]], dim=1)
    return (loss**2).mean()

def normal_cosine_loss(views, gbuffers):
    """ Compute the normal consistency term as the cosine similarity between deformed vertices

    Args:
        mesh (Mesh): Mesh with face normals.
    """
    loss = 0
    for view, gbuffer in zip(views, gbuffers):
        deformed_normals = gbuffer["normal"] * view.skin_mask
        gt_normals = view.normals * view.skin_mask
        loss += 1 - torch.cosine_similarity(deformed_normals.view(-1, 3), gt_normals.view(-1, 3), dim=1)
    return (loss**2).mean()