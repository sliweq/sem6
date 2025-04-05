import MainMenu from './components/MainMenu.vue';
import AuthorsList from './pages/AuthorsList.vue';
import RentalList from './pages/RentalList.vue';
import BooksAdd from './pages/BooksAdd.vue';
import BookEdit from './pages/BookEdit.vue';
import AuthorAdd from './pages/AuthorAdd.vue';
import AuthorEdit from './pages/AuthorEdit.vue';
import RentalAdd from './pages/RentalAdd.vue';
import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '@/layouts/MainLayout.vue';
import BooksList from './pages/BooksList.vue';
import LoginLayout from './layouts/LoginLayout.vue';
import LoginPage from '@/pages/LoginPage.vue';

const routes = [
  {
    path: '/',
    component: MainLayout, 
    children: [
      { path: '', component: MainMenu },
      { path: 'books', component: BooksList },
      { path: '/add-book', component: BooksAdd },
      { path: '/edit-book/:id', component: BookEdit },
      { path: '/authors', component: AuthorsList },
      { path: '/rentals', component: RentalList },
      { path: '/add-author', component: AuthorAdd },
      { path: '/edit-author/:id', component: AuthorEdit },
      { path: '/add-rental', component: RentalAdd },
    ],
  },
  {
    path: '/login',
    component: LoginLayout, 
    children: [{ path: '', component: LoginPage }],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
