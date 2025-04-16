from ..core import *

class Components:

    @staticmethod
    def generate_select_components_for_pages(options: list, custom_id, placeholder, fields_for_one: int = 25,
                                             category=None):
        fields_for_one -= 1
        components = []
        generated_options = []

        if not options:
            return [components]

        def append_components(page: int = 1):
            components.append([
                discord.ui.Select(options=generated_options, custom_id=f'{custom_id};{category};{page}',
                                  placeholder=placeholder)])

        c = 1
        for i, option in enumerate(options, 1):
            generated_options.append(discord.SelectOption(
                label=option['label'],
                value=option['value'],
                emoji=option['emoji'],
                description=option['description']
            ))
            if i % (fields_for_one + 1) == 0:
                append_components(c)
                generated_options = []
                c += 1
        if generated_options:
            append_components(c)
        else:
            components.append([])
        return components