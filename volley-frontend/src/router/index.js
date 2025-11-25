import {createRouter, createWebHistory} from 'vue-router';


const routes = [
  {path: '/', name: 'Home', component: () => import('../views/Home.vue')},
  {path: '/players', name: 'Players', component: () => import('../components/Players.vue')},
  {path: '/players/:id', name: 'Player', component: () => import('../components/Player.vue'), props: true},
  {path: '/new-player', name: 'NewPlayer', component: () => import('../components/forms/NewPlayer.vue')},
  {path: '/games', name: 'Games', component: () => import('../components/Games.vue')},
  {path: '/games/:id', name: 'Game', component: () => import('../components/Game.vue'), props: true},
  {path: '/new-game', name: 'NewGame', component: () => import('../components/forms/NewGame.vue')},
  {path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../views/NotFound.vue')},
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;