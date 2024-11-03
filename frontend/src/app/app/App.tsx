// import { Outlet } from 'react-router-dom';

import { Header } from '../../features/Header/Header';
import { Outlet } from 'react-router-dom';

export function App() {
  return (
    <>
      <Header />
      <main className="App-Main">
        <Outlet />
      </main>
    </>
  );
}
