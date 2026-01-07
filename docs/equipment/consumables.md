---
title: Consumables
---
<template id="sidebar-extra">
  <div class="sidebar-extra sidebar-extra-larger">
    <h3>Navigation</h3>
    <hr>
    <p>
    <a href="#consumables-potions">Potions</a>
    <br><a href="#consumables-tonics">Tonics</a>
    <br><a href="#consumables-poisons">Poisons</a>
    <br><a href="#consumables-food">Food</a>
    </p>
  </div>
</template>

# Consumables
Most consumables (except food) are alchemical concoctions that need to enter the body to take effect, be it through literal consumption or through more invasive methods like poisoned arrows.

### Save
To save against an unwanted effect, the affected creature must perform a <span class="clr-attr">CON</span> save against a <span class="clr-dc">DC</span> of [<span class="clr-value">10</span> + the consumable's <span class="clr-value">quality score (Q)</span>].
<br>Exempt from this are consumables that cause DoT and HoT status effects, like <i>Bleeding</i> or <i>Regeneration</i>. In these cases, the status effect rules apply.

### Cleansing
To cleanse the effect of a consumable (positive or negative) with a spell like <i>Purify</i>, a <span class="clr-dc">DC</span> of [<span class="clr-value">20</span> + the affected creature's <span class="clr-attr">CON-MOD</span>] must be reached.

---
## Potions
Potions are consumables with a one-time effect.
{{ table('data/tables/items/consumables-potions.yaml') }}

---
## Tonics
The effects of tonics last for an entire Phase.
{{ table('data/tables/items/consumables-tonics.yaml') }}

---
## Poisons
In combat, poisons are usually delivered through invasive means like poisoned arrows and blades.
<br>Out of combat, poisons are generally involuntarily consumed, in which case all saves made against them are <a href="/generia/rules/basic/core-mechanics#Hindered">hindered</a> by <span class="clr-value">10</span>, including saves against the regular status effect <i>Poisoned</i>.
{{ table('data/tables/items/consumables-poisons.yaml') }}

---
## Food
Food is the best (and least expensive) way to regenerate <span class="clr-en">Energy</span>. Below are rough categories of food adventurers consume, with snacks and field rations being the most common and cheapest by a wide margin, though not necessarily the tastiest...
{{ table('data/tables/items/consumables-food.yaml') }}