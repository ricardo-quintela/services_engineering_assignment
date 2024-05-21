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
import { jwtDecode } from "jwt-decode";
import { JwtPayload } from "../interfaces/jwt";
import LandingPage from "./LandingPage";
import AppointementsDashboard from "./AppointementsDashboard";
import CameraFeed from "./CameraFeed";
import axios from "axios";
import Profile from "./Profile";

const App = () => {
    const addNotification = (notificationData: NotificationData) =>
        setNotificationQueue([...notificationQueue, notificationData]);

    const closeNotification = (index: number) =>
        setNotificationQueue(notificationQueue.filter((_, i) => i !== index));

    const [notificationQueue, setNotificationQueue] = useState(
        [] as NotificationData[]
    );

    // restore token
    if (localStorage.getItem("jwt") !== null) {
        axios.defaults.headers.common["jwt"] = localStorage.getItem("jwt");
    }

    const checkAdmin = () =>
        (localStorage.getItem("jwt") &&
            (jwtDecode(localStorage.getItem("jwt") || "") as JwtPayload)
                .role) === "admin";

    const checkCommonUser = () =>
        (localStorage.getItem("jwt") &&
            (jwtDecode(localStorage.getItem("jwt") || "") as JwtPayload).role) !== "admin";

	const checkLogin = () => localStorage.getItem("jwt") !== "";

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
                            path="/profile"
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
                                    <Profile
                                        addNotification={addNotification}
                                    />
                                </ProtectedRoute>
                            }
                        />
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
                        <Route
                            path="/list_appointements"
                            element={
                                <ProtectedRoute
                                    condition={checkCommonUser}
                                    redirectTo="/"
                                    addNotification={addNotification}
                                    notificationData={{
                                        title: "Acesso Negado",
                                        message:
                                            "Não tem permissões para aceder a este recurso.",
                                    }}
                                >
                                    <AppointementsDashboard
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
