import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def buffs(inter, _global: bool = False):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    await Utils.pagination(inter, lang,
                           embeds={
                               translate(Locales.Buffs.main_page_title, lang): {
                                   'embed': await embeds.generate_basic_buffs_embed(inter, lang,
                                                                                    thumbnail_url=await Func.get_image_temp_path_from_path_or_link(
                                                                                        utils_config.image_links[
                                                                                            'buffs']))},
                               translate(Locales.Buffs.weight_buffs_title, lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='weight',
                                                                                          thumbnail_url=await Func.get_image_temp_path_from_path_or_link(
                                                                                              utils_config.image_links[
                                                                                                  'buffs']))},
                               translate(Locales.Buffs.pooping_buffs_title, lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='pooping',
                                                                                          thumbnail_url=await Func.get_image_temp_path_from_path_or_link(
                                                                                              utils_config.image_links[
                                                                                                  'buffs']))},
                               translate(Locales.Buffs.vomit_chance_buffs_title, lang): {
                                   'embed': await embeds.generate_buffs_multipliers_embed(inter, lang,
                                                                                          buff_type='vomit_chance',
                                                                                          thumbnail_url=await Func.get_image_temp_path_from_path_or_link(
                                                                                              utils_config.image_links[
                                                                                                  'buffs']))}
                           },
                           arrows=False,
                           categories=True)
