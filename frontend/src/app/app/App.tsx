// import { Outlet } from 'react-router-dom';

import { Auth } from '../../features/Auth/Auth';
import { DevInfoShortCard } from '../../features/DevInfo/DevInfoShortCard';
import { Header } from '../../features/Header/Header';
import { Outlet } from 'react-router-dom';

export function App() {
  return (
    <>
      <Header />
      <main className="App-Main">
        <DevInfoShortCard />
        <Outlet />
      </main>
      <Auth />
    </>
  );
}
