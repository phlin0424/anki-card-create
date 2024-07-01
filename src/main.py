import argparse
from config import settings
from card_creator import AnkiNotes, CardCreator
import logging

logging.basicConfig(level=logging.INFO)


def get_args_parser(known=False):
    parser = argparse.ArgumentParser("Create Anki flash cards.")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-f",
        "--file",
        help="File containing text for Anki cards.",
    )
    group.add_argument(
        "-w",
        "--word",
        help="The vocabulary for Anki cards.",
    )

    parser.add_argument(
        "-d",
        "--deck_name",
        default=settings.deck_name,
        help="Name of the Anki deck to which the cards will be added.",
    )
    parser.add_argument(
        "-m",
        "--model_name",
        default=settings.model_name,
        help="Name of the Anki card model to which the cards will be added.",
    )

    # Arguments to update the
    parser.add_argument(
        "--set-deck-name",
        help="Set a new default deck name for the Anki cards.",
    )

    parser.add_argument(
        "--set-model-name",
        help="Set a new default model name of the Anki cards.",
    )

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


def main():
    args = get_args_parser(known=True)

    if args.set_deck_name:
        settings.deck_name = args.set_deck_name

    if args.set_model_name:
        settings.model_name = args.set_model_name

    logging.info(f"deck name: {args.deck_name}; card model: {args.model_name}")

    if args.file:
        anki_notes = AnkiNotes.from_txt(
            data_fname=args.file,
            deck_name=args.deck_name,
            model_name=args.model_name,
        ).anki_notes
    else:
        anki_notes = AnkiNotes.from_input_word(
            input_str=args.word,
            deck_name=args.deck_name,
            model_name=args.model_name,
        ).anki_notes

    card_creator = CardCreator(anki_notes)
    response_list = card_creator.send_notes(audio=True)


if __name__ == "__main__":
    main()
