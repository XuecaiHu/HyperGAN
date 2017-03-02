import tensorflow as tf
from hypergan.util.ops import *
from hypergan.util.hc_tf import *
import hyperchamber as hc

from hypergan.losses import wgan_loss, standard_gan_loss

def config(
        reduce=tf.reduce_mean, 
        reverse=False,
        discriminator=None,
        label_smooth=list(np.linspace(0.15, 0.35, num=10)),
        alpha=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    ):
    selector = hc.Selector()
    selector.set("reduce", reduce)
    selector.set('reverse', reverse)
    selector.set('discriminator', discriminator)
    selector.set("label_smooth", label_smooth)
    selector.set('create', create)
    selector.set('alpha', alpha)

    return selector.random_config()

def create(config, gan):
    alpha = config.alpha
    wgan_loss_d, wgan_loss_g = wgan_loss.create(config, gan)
    config['reduce']=standard_gan_loss.linear_projection
    standard_loss_d, standard_loss_g = standard_gan_loss.create(config, gan)

    d_loss = wgan_loss_d*alpha + (1-alpha)*standard_loss_d
    g_loss = wgan_loss_g*alpha + (1-alpha)*standard_loss_g

    return [d_loss, g_loss]
