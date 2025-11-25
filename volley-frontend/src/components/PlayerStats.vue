<template>
  <div v-if="stats">
    <h2>Statistiky hráče {{ stats.id }}</h2>
    <ul>
      <li>Celkem her: {{ stats.total_games }}</li>
      <li>Výhry: {{ stats.wins }}, Prohry: {{ stats.losses }}</li>
      <li>Win rate: {{ (stats.win_rate * 100).toFixed(1) }} %</li>
      <li>Výhry v týmu 1: {{ stats.wins_team1 }}, tým 2: {{ stats.wins_team2 }}</li>
      <li>Prům. skóre ve hrách: {{ stats.avg_score_for.toFixed(1) }} – {{ stats.avg_score_against.toFixed(1) }}</li>
      <li>Prům. skóre ve výhrách: {{ stats.avg_score_for_wins.toFixed(1) }}</li>
      <li>Prům. skóre v prohrách: {{ stats.avg_score_against_losses.toFixed(1) }}</li>
      <li>Celkem setů: {{ stats.total_sets }}</li>
      <li>Vyhraných setů: {{ stats.sets_won }}, Prohraných: {{ stats.sets_lost }}</li>
      <li>Set win rate: {{ (stats.sets_win_rate * 100).toFixed(1) }} %</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  playerId: Number
})

const stats = ref(null)

async function fetchStats(id) {
  const res = await fetch(`http://localhost:8000/players/${id}/stats`)
  stats.value = await res.json()
}

watch(() => props.playerId, id => {
  if (id) fetchStats(id)
})
</script>
