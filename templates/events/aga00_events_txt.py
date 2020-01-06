from templates.utils import settings, templater

species_selector = """
			{if_statement} = {{
				limit = {{
					root = {{
						count_owned_pops = {{
							count >= {count}
							limit = {{
								is_being_purged = no
								OR = {{
									is_same_species = prev
									is_subspecies = prev
								}}
							}}
						}}
					}}
				}}
				root = {{
					random_owned_pop_species = {{
						limit = {{
							count_pops = {{
								count >= {count}
								limit = {{
									is_being_purged = no
									OR = {{
										is_same_species = prevprev
										is_subspecies = prevprev
									}}
								}}
							}}
						}}
						root = {{
							### Sets flags to all species once and then 0112 sifts out flags for unsuitable species.
							every_owned_pop_species = {{
								limit = {{
									is_same_species = prevprevprevprev
								}}
								set_species_flag = AgaFlagGeneAssimilationStandardSpecies@root
							}}
						}}
					}}
				}}
			}}"""


def process(publish_dir):
    species_selector_lines = []

    for i in range(settings.max['range'], settings.middle['range'], settings.max['step']):
        if i == settings.max['range']:
            species_selector_lines.append(
                species_selector.format(count=i, if_statement="if"))
        else:
            species_selector_lines.append(
                species_selector.format(count=i, if_statement="else_if"))

    for i in range(settings.middle['range'], settings.low['range'], settings.middle['step']):
        species_selector_lines.append(
            species_selector.format(count=i, if_statement="else_if"))
    for i in range(settings.low['range'], 0, settings.low['step']):
        species_selector_lines.append(
            species_selector.format(count=i, if_statement="else_if"))

    templater.process_file(
        publish_dir + "/events/Aga00_events.txt",
        species_selector=species_selector_lines)
