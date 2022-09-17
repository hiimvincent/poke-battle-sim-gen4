import csv
import random
import global_settings as gs

class PokeSim:
    _pokemon_stats = []
    _name_to_id = {}
    _natures = {}
    _move_list = []
    _move_name_to_id = {}
    _type_effectives = []
    _type_to_id = {}
    _abilities = {}

    @classmethod
    def start(cls):
        #error handling?
        with open(gs.POKEMON_STATS_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                for num in gs.POKEMON_STATS_NUMS:
                    row[num] = int(row[num])
                cls._pokemon_stats.append(row)
                cls._name_to_id[row[1]] = row[0]

        with open(gs.NATURES_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                cls._natures[row[0]] = (int(row[1]), int(row[2]))

        with open(gs.MOVES_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                for num in gs.MOVES_NUM:
                    if row[num]:
                        row[num] = int(row[num])
                cls._move_list.append(row)
                cls._move_name_to_id[row[1]] = row[0]

        with open(gs.TYPE_EF_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            line_count = 0
            for row in csv_reader:
                cls._type_to_id[row[0]] = line_count
                row = [float(row[i]) for i in range(1, len(row))]
                cls._type_effectives.append(row)
                line_count += 1

        with open(gs.ABILITIES_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                cls._abilities[row[1]] = (row[0], row[2])

    @classmethod
    def _convert_name_to_id(cls, name: str) -> int:
        if name not in cls._name_to_id:
            return -1
        return cls._name_to_id[name]

    @classmethod
    def get_valid_name_or_id(cls, name_or_id: str | int) -> int | None:
        if not isinstance(name_or_id, (str, int)):
            return
        p_id = name_or_id
        if isinstance(name_or_id, str):
            p_id = cls._convert_name_to_id(name_or_id)
        if 0 < p_id < len(cls._pokemon_stats):
            return p_id
        return

    @classmethod
    def get_pokemon(cls, name_or_id: str | int) -> list | None:
        p_id = cls.get_valid_name_or_id(name_or_id.lower())
        if not p_id:
            return
        return cls._pokemon_stats[p_id - 1]

    @classmethod
    def nature_conversion(cls, nature: str) -> tuple[int, int] | None:
        if not isinstance(nature, str) or nature not in cls._natures:
            return
        return cls._natures[nature]

    @classmethod
    def get_move_data(cls, moves: [str]) -> list | None:
        if not isinstance(moves, list):
            return
        move_data = []
        move_ids = []
        for move in moves:
            if move not in cls._move_name_to_id:
                return
            move_data.append(cls._move_list[cls._move_name_to_id[move] - 1])
            if move_data[-1][0] in move_ids:
                return
            move_ids.append(move_data[-1][0])
        return move_data

    @classmethod
    def check_status(cls, status: str):
        return

    @classmethod
    def get_type_effectiveness(cls, move_type: str, def_type: str) -> float | None:
        if move_type not in cls._type_to_id or def_type not in cls._type_to_id:
            return
        return cls._type_effectives[cls._type_to_id[move_type]][cls._type_to_id[def_type]]

    @classmethod
    def get_all_types(cls) -> list:
        return cls._type_to_id.keys()

    @classmethod
    def get_rand_move(cls) -> list:
        return cls._move_list[random.randrange(gs.COMPLETED_MOVES + 1)]

    @classmethod
    def check_ability(cls, ability: str) -> bool:
        return ability in cls._abilities