---
title: Price Lists
---
<template id="sidebar-extra">
  <div class="sidebar-extra sidebar-extra-larger">
    <h3>Navigation</h3>
    <hr>
    <h4>Weapons</h4>
    <p>
    <a href="#BluntWeaponsCommon">Blunt</a>
    <br><a href="#SlashingWeaponsCommon">Slashing</a>
    <br><a href="#StabbingWeaponsCommon">Stabbing</a>
    <br><a href="#RangedWeaponsCommon">Ranged</a>
    <br><a href="#DefensiveWeaponsCommon">Defensive</a>
    <br><a href="#NaturalWeaponsBasic">Natural</a>
    <br><a href="#AmmunitionCommon">Ammunition</a>
    </p>
    <h4>Armor</h4>
    <p>
    <a href="#armor-light">Light Armor</a>
    <br><a href="#armor-medium">Medium Armor</a>
    <br><a href="#armor-heavy">Heavy Armor</a>
    </p>
    <h4>Consumables</h4>
    <p>
    <a href="#consumables-potions">Potions</a>
    <br><a href="#consumables-tonics">Tonics</a>
    <br><a href="#consumables-poisons">Poisons</a>
    <br><a href="#consumables-food">Food</a>
    </p>
    <h4>Materials & Tools</h4>
    <p>
    <a href="#items-materials">Materials</a>
    <br><a href="#items-tools">Tools</a>
    <br><a href="#items-exploration">Exploration</a>
    </p>
  </div>
</template>

# Price Lists

## Weapons
{{ price_table('data/tables/weapons/weapons-blunt-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-blunt-rare.yaml') }}
{{ price_table('data/tables/weapons/weapons-slashing-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-slashing-rare.yaml') }}
{{ price_table('data/tables/weapons/weapons-stabbing-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-stabbing-rare.yaml') }}
{{ price_table('data/tables/weapons/weapons-ranged-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-ranged-rare.yaml') }}
{{ price_table('data/tables/weapons/weapons-defensive-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-ammunition-common.yaml') }}
{{ price_table('data/tables/weapons/weapons-ammunition-rare.yaml') }}

## Armor
{{ price_table('data/tables/armor/armor-light.yaml') }}
{{ price_table('data/tables/armor/armor-medium.yaml') }}
{{ price_table('data/tables/armor/armor-heavy.yaml') }}

## Consumables
{{ price_table('data/tables/items/consumables-potions.yaml') }}
{{ price_table('data/tables/items/consumables-tonics.yaml') }}
{{ price_table('data/tables/items/consumables-poisons.yaml') }}
{{ price_table('data/tables/items/consumables-food.yaml') }}

## Materials & Tools
{{ price_table('data/tables/items/items-materials.yaml') }}
{{ price_table('data/tables/items/items-tools.yaml') }}
{{ price_table('data/tables/items/items-exploration.yaml') }}