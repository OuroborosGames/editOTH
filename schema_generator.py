import json

import jsl
from functools import partial

ref = partial(jsl.DocumentField, as_ref=True)
attr_dict = {'health': jsl.IntField(), 'technology': jsl.IntField(), 'safety': jsl.IntField(), 'food': jsl.IntField(),
             'prestige': jsl.IntField(), 'money': jsl.IntField()}


# proper definitions
class Building(jsl.Document):
    class Options(object):
        title = 'Building'
    building_name = jsl.StringField(required=True)
    description = jsl.StringField()
    base_price = jsl.IntField(required=True)
    additional_effects = jsl.DictField(additional_properties=True,properties=attr_dict)
    per_turn_effects = jsl.DictField(additional_properties=True, properties=attr_dict)


class TerrainRestrictedBuilding(Building):
    class Options(object):
        title = 'Terrain Restricted Building'
    required_tile = jsl.StringField(required=True, enum=["Water", "Grass", "Forest", "Hills", "Mountains"])


class CustomBuilding(Building):
    class Options(object):
        title = 'Custom Building'
    build_predicate = jsl.StringField(required=True)


# this is a setup for a reallly awful hack
class IndirectActionToTake(jsl.Document):
    pass


class IndirectTextEvent(jsl.Document):
    pass


class IndirectUnlockableEvent(jsl.Document):
    pass


class IndirectConditionalEvent(jsl.Document):
    pass


class Predicate(jsl.Document):
    predicate = jsl.StringField(
        enum=["counter_greater", "counter_lower", "counter_equal", "attr_greater", "attr_lower", "attr_equal"],
        required=True)
    key = jsl.StringField(required=True)
    value = jsl.IntField(required=True)


class SpawnImmediately(jsl.Document):
    class Options(object):
        title = 'Spawn event'
    event = jsl.OneOfField([ref(IndirectTextEvent), ref(IndirectUnlockableEvent), ref(IndirectConditionalEvent)],
                           required=True)


class AddEvent(SpawnImmediately):
    class Options(object):
        title = 'Add random event'
    active = jsl.BooleanField(required=True)


class SpawnAfterNTurns(SpawnImmediately):
    class Options(object):
        title = 'Spawn an event after a number of turns'
    turns = jsl.IntField()


class SpawnNextSeason(SpawnImmediately):
    class Options(object):
        title = 'Spawn an event during a chosen season'
    season = jsl.IntField(minimum=0, maximum=3)


class ModifyState(jsl.Document):
    class Options(object):
        title = 'Increase/decrease stats'
    attributes = jsl.DictField(properties=attr_dict)


class UnlockBuilding(jsl.Document):
    class Options(object):
        title = 'Unlock a new building'
    building = jsl.OneOfField([ref(Building), ref(TerrainRestrictedBuilding), ref(CustomBuilding)])


class SpecialAction(jsl.Document):
    class Options(object):
        title = 'Special action'
    name = jsl.StringField(required=True)
    description = jsl.StringField()
    event = jsl.OneOfField([ref(IndirectTextEvent), ref(IndirectUnlockableEvent), ref(IndirectConditionalEvent)],
                           required=True)


class LimitedAction(SpecialAction):
    class Options(object):
        title = 'Limited special action'
    limit = jsl.IntField(required=True)


class UnlockAction(jsl.Document):
    class Options(object):
        title = 'Unlock a special action'
    action = jsl.OneOfField([ref(SpecialAction), ref(LimitedAction)])


class ActionToTake(jsl.Document):
    name = jsl.StringField(required=True)
    effect = jsl.OneOfField([ref(SpawnImmediately), ref(AddEvent), ref(SpawnAfterNTurns), ref(SpawnNextSeason),
                            ref(ModifyState), ref(UnlockBuilding), ref(UnlockAction)])


class TextEvent(jsl.Document):
    class Options(object):
        title = 'Basic text event'
    event_title = jsl.StringField(required=True)
    description = jsl.StringField()
    actions = jsl.ArrayField(items=[ref(ActionToTake)])


class UnlockableEvent(TextEvent):
    class Options(object):
        title = 'Unlockable event'
    unlock_predicate = ref(Predicate, required=True)


class ConditionalEvent(TextEvent):
    class Options(object):
        title = 'Conditional Event'
    condition = ref(Predicate, required=True)


class BasicBuildings(jsl.Document):
    class Options(object):
        title = 'Basic Buildings'
    buildings = jsl.ArrayField(items=jsl.OneOfField([jsl.DocumentField(Building),
                                                     jsl.DocumentField(TerrainRestrictedBuilding),
                                                     jsl.DocumentField(CustomBuilding)]))


class Events(jsl.Document):
    class Options(object):
        title = 'Text-based events'
    events = jsl.ArrayField(items=jsl.OneOfField([jsl.DocumentField(TextEvent), jsl.DocumentField(UnlockableEvent),
                                                  jsl.DocumentField(ConditionalEvent)]))

# class InitialActions(jsl.Document):
#     content = jsl.ArrayField(items=jsl.OneOfField([ref(SpecialAction), ref(LimitedAction)]))


class Content(jsl.Document):
    class Options(object):
        title = 'Game contents'
    contents = jsl.ArrayField(items=jsl.OneOfField([ref(TextEvent), ref(UnlockableEvent), ref(ConditionalEvent),
                                                    ref(Building), ref(TerrainRestrictedBuilding),
                                                    ref(CustomBuilding)]))

def main():
    schema = Content.get_schema(ordered=True)
    # a horrible hack for getting circular indirect references to work
    for d in list(schema['definitions'].keys()):
        if 'Indirect' in d:
            del schema['definitions'][d]
    with open("editor.html", 'w') as f:
        f.write(
            "<html><head><title>On The Hill content editor</title><script src=\"jsoneditor.js\"></script></head>")
        f.write("<body><div id = \'editor_holder\'></div><script>")
        f.write("var editor = new JSONEditor(document.getElementById(\'editor_holder\'), {schema: ")
        f.write(json.dumps(schema).replace("Indirect", ""))
        f.write("});</script></body></html>")

if __name__ == "__main__":
    main()
