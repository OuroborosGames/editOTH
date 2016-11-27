import json

import jsl
from functools import partial

ref = partial(jsl.DocumentField, as_ref=True)


# prototypes to avoid compiler butthurt
# class SpawnImmediately(jsl.Document):
#     pass
#
#
# class AddEvent(jsl.Document):
#     pass
#
#
# class SpawnAfterNTurns(jsl.Document):
#     pass
#
#
# class SpawnNextSeason(jsl.Document):
#     pass
#
#
# class ModifyState(jsl.Document):
#     pass
#
#
# class UnlockBuilding(jsl.Document):
#     pass
#
#
# class UnlockAction(jsl.Document):
#     pass


# proper definitions
class Building(jsl.Document):
    class Options(object):
        title = 'Building'
    name = jsl.StringField(required=True)
    description = jsl.StringField()
    base_price = jsl.IntField(required=True)
    additional_effects = jsl.DictField(additional_properties=True)
    per_turn_effects = jsl.DictField(additional_properties=True)


class TerrainRestrictedBuilding(Building):
    class Options(object):
        title = 'Terrain Restricted Building'
    required_tile = jsl.StringField(required=True)


class CustomBuilding(Building):
    class Options(object):
        title = 'Custom Building'
    build_predicate = jsl.StringField(required=True)


# class Predicate(jsl.Document):
#     predicate = jsl.StringField(
#         pattern="/^(counter_greater|counter_lower|counter_equal|attr_greater|attr_lower|attr_equal)$/",
#         required=True)
#     key = jsl.StringField(required=True)
#     value = jsl.IntField(required=True)
#
#
# class ActionToTake(jsl.Document):
#     name = jsl.StringField(required=True)
#     effect = jsl.OneOfField([ref(SpawnImmediately), ref(AddEvent), ref(SpawnAfterNTurns), ref(SpawnNextSeason),
#                             ref(ModifyState), ref(UnlockBuilding), ref(UnlockAction)])
#
#
# class TextEvent(jsl.Document):
#     title = jsl.StringField(required=True)
#     description = jsl.StringField()
#     actions = jsl.ArrayField(items=[ref(ActionToTake)])
#
#
# class UnlockableEvent(TextEvent):
#     unlock_predicate = ref(Predicate, required=True)
#
#
# class ConditionalEvent(TextEvent):
#     condition = ref(Predicate, required=True)
#
#
# class SpawnImmediately(jsl.Document):
#     event = jsl.OneOfField([ref(TextEvent), ref(UnlockableEvent), ref(ConditionalEvent)], required=True)
#
#
# class AddEvent(SpawnImmediately):
#     active = jsl.BooleanField(required=True)
#
#
# class SpawnAfterNTurns(SpawnImmediately):
#     turns = jsl.IntField()
#
#
# class SpawnNextSeason(SpawnImmediately):
#     season = jsl.IntField(minimum=0, maximum=3)
#
#
# class ModifyState(jsl.Document):
#     attributes = jsl.DictField()
#
#
# class UnlockBuilding(jsl.Document):
#     building = jsl.OneOfField([ref(Building), ref(TerrainRestrictedBuilding), ref(CustomBuilding)])
#
#
# class SpecialAction(jsl.Document):
#     name = jsl.StringField(required=True)
#     description = jsl.StringField()
#     event = jsl.OneOfField([ref(TextEvent), ref(UnlockableEvent), ref(ConditionalEvent)], required=True)
#
#
# class LimitedAction(SpecialAction):
#     limit = jsl.IntField(required=True)
#
#
# class UnlockAction(jsl.Document):
#     action = jsl.OneOfField([ref(SpecialAction), ref(LimitedAction)])
#
#
class BasicBuildings(jsl.Document):
    class Options(object):
        title = 'Basic Buildings'
    content = jsl.ArrayField(items=jsl.OneOfField([jsl.DocumentField(Building),
                                                   jsl.DocumentField(TerrainRestrictedBuilding),
                                                   jsl.DocumentField(CustomBuilding)]))


# class InitialActions(jsl.Document):
#     content = jsl.ArrayField(items=jsl.OneOfField([ref(SpecialAction), ref(LimitedAction)]))
#
#
# class Events(jsl.Document):
#     content = jsl.ArrayField(items=jsl.OneOfField([ref(TextEvent), ref(UnlockableEvent), ref(ConditionalEvent)]))


def main():
    with open('buildings.jschema', 'w') as f:
        json.dump(BasicBuildings.get_schema(ordered=True), f, indent=4, separators=(',', ': '))
    # with open('actions.jschema', 'w') as f:
    #     json.dump(InitialActions.get_schema(ordered=True), f) #, indent=4, separators=(',', ': '))
    # with open('events.jschema', 'w') as f:
    #     json.dump(Events.get_schema(ordered=True), f) #, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    main()
