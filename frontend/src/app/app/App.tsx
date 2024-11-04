import { Auth } from '../../features/Auth/Auth';
import { DevFullCard } from '../../features/DevInfo/DevFullCard';
import { Header } from '../../features/Header/Header';
import { Outlet } from 'react-router-dom';
import Form from '../../features/Team/CreateTeamForm';

export function App() {
  return (
    <>
      <Header />
      <main className="App-Main">
        <DevFullCard username="Ten-Do" />
        <Outlet />
      </main>
      <Auth />
      <Form />
    </>
  );
}
