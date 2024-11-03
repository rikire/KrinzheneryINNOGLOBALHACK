import { createBrowserRouter } from 'react-router-dom';
import { App } from './app/App';
import ErrorPage from './error/error';
import { DeveloperPage } from './developer/page';
import { SearchPage } from './search/page';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: '/developer/:username',
        element: <DeveloperPage />,
      },
      {
        path: '/search/:competencies',
        element: <SearchPage />,
      },
    ],
  },
]);
