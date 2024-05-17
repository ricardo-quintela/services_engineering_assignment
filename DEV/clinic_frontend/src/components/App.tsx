import { useState } from "react";
import LoginForm from "./LoginForm";
import NavBar from "./NavBar";
import AdminDashboard from "./AdminDashboard";
import { NotificationData } from "../interfaces/notification";
import NotificationManager from "./NotificationManager";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import SchedullingForm from "./SchedullingForm";
import RegisterForm from "./RegisterForm";
import ProtectedRoute from "./ProtectedRoute";
import { getCookies } from "../cookies";
import { jwtDecode } from "jwt-decode";
import { JwtPayload } from "../interfaces/jwt";
import LandingPage from "./LandingPage";

const App = () => {
    const addNotification = (notificationData: NotificationData) =>
        setNotificationQueue([...notificationQueue, notificationData]);

    const closeNotification = (index: number) =>
        setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

    const [notificationQueue, setNotificationQueue] = useState(
        [] as NotificationData[]
    );

    const checkAdmin = () =>
        (getCookies()["jwt"] &&
            (jwtDecode(getCookies()["jwt"]) as JwtPayload).role) === "admin";

	const checkLogin = () => getCookies()["jwt"] !== "";

    return (
        <>
            {/* inner content of the page */}
            <BrowserRouter>
                {/* nav bar */}
                <NavBar />

                <section className="h-75">
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route
                            path="/scheduling"
                            element={
                                <ProtectedRoute
                                    condition={checkLogin}
                                    redirectTo="/"
                                    addNotification={addNotification}
                                    notificationData={{
                                        title: "Acesso Negado",
                                        message:
                                            "Precisa de fazer login para aceder a este recurso.",
                                    }}
                                >
                                    <SchedullingForm />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/login"
                            element={
                                <LoginForm
                                    key={0}
                                    addNotification={addNotification}
                                />
                            }
                        />
                        <Route
                            path="/register"
                            element={
                                <RegisterForm
                                    key={0}
                                    addNotification={addNotification}
                                />
                            }
                        />
                        <Route
                            path="/admin"
                            element={
                                <ProtectedRoute
                                    condition={checkAdmin}
                                    redirectTo="/"
                                    addNotification={addNotification}
                                    notificationData={{
                                        title: "Acesso Negado",
                                        message:
                                            "Não tem permissões para aceder a este recurso.",
                                    }}
                                >
                                    <AdminDashboard
                                        key={0}
                                        addNotification={addNotification}
                                    />
                                </ProtectedRoute>
                            }
                        />
                    </Routes>
                </section>

                {/* handle notifications */}
                <NotificationManager
                    notificationQueue={notificationQueue}
                    closeNotification={closeNotification}
                />
            </BrowserRouter>
        </>
    );
};

export default App;
