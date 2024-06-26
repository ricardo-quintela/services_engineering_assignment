import axios, { AxiosResponse } from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Badge, Button, Container } from "react-bootstrap";
import { NotificationData } from "../interfaces/notification";
import ListGroup from "react-bootstrap/ListGroup";
import { AppointmentData } from "../interfaces/appointment";
import CameraFeed from "./CameraFeed";

axios.defaults.withCredentials = true;

const AdminDashboard = ({
    addNotification,
}: {
    addNotification: (notificationData: NotificationData) => void;
}) => {
    const [appointmentData, setAppointmentData] = useState(
        [] as AppointmentData[]
    );
    const [ranQuery, setRanQuery] = useState(false);

    if (!ranQuery) {
        axios
            .get(process.env.REACT_APP_API_URL + "appointments/")
            .then((response) => {
                if ("error" in response.data) {
                    addNotification({
                        title: "Error",
                        message: response.data["error"],
                    });
                    return;
                }

                setAppointmentData(response.data);
                setRanQuery(true);
            })
            .catch(() =>
                addNotification({
                    title: "Erro",
                    message: "Não foi possível obter os dados das consultas.",
                })
            );
    }

    const handleCloseAppointment = (appointmentId: number, index: number) => {
        axios
            .put(
                process.env.REACT_APP_API_URL +
                    `appointments/${appointmentId}/`,
                { estado: "closed" }
            )
            .then((response) => {
                if ("error" in response.data) {
                    addNotification({
                        title: "Erro",
                        message: response.data["error"],
                    });
                    return;
                }

                setAppointmentData(
                    appointmentData.map((data, i) => {
                        if (i !== index) return data;
                        return response.data;
                    })
                );
            })
            .catch(() =>
                addNotification({
                    title: "Erro",
                    message: "Ocorreu um erro ao fechar a consulta.",
                })
            );
    };

    const handleOnGoingAppointment = (appointmentId: number) => {
        axios
            .put(
                process.env.REACT_APP_API_URL +
                    `appointments/${appointmentId}/`,
                { estado: "ongoing" }
            )
            .then((response) => {
                if ("error" in response.data) {
                    addNotification({
                        title: "Erro",
                        message: response.data["error"],
                    });
                    return;
                }
                setAppointmentData( [] as AppointmentData[] );
                setRanQuery(false);
                addNotification({
                    title: "Success",
                    message: "A clínica foi informada da sua entrada, aguarde pela chamada.",
                });
            })
            .catch(() =>
                addNotification({
                    title: "Erro",
                    message: "Ocorreu um erro ao procurar a sua consulta.",
                })
            );
    };

    const handleFacialRecognitionResponse = (response: AxiosResponse) => {
        if ("message" in response.data) {
            addNotification({
                title: "Sucesso",
                message: `Cliente autenticado: ${response.data["message"]}`
            });

            // TODO: search for an appointement in this date search_id/username
            const url = process.env.REACT_APP_API_URL + `search_id/${response.data["message"]}`;
            axios.get(
                url
            )
            .then((response) => {
                handleOnGoingAppointment(response.data["id"]);
            })
            .catch(() => {
                addNotification({
                    title: "Erro",
                    message: "Ocorreu um erro ao procurar a consulta.",
                })
            })
            return;
        }

        addNotification({
            title: "Erro",
            message: "Cliente não reconhecido."
        });
    };

    return (
        <div className="d-flex gap-5 flex-column h-75 align-items-sm-start align-items-center">
            <div>
                <h1>Lista de Consultas</h1>
                <ListGroup as="ol" numbered>
                    {appointmentData.length === 0 && (
                        <p>Não existem consultas.</p>
                    )}
                    {appointmentData.map((data, index) => (
                        <ListGroup.Item
                            key={data.id}
                            as="li"
                            className="d-flex flex-sm-row flex-column justify-content-between align-items-sm-center gap-3"
                        >
                            <div className="ms-2 me-auto">
                                <div className="fw-bold d-flex gap-2">
                                    {data.user.username}
                                    {data.estado !== "closed" && (
                                        <Badge bg="primary" pill>
                                            {
                                                {
                                                    open: "Aberta",
                                                    ongoing: "A decorrer",
                                                    payed: "Paga",
                                                }[data.estado]
                                            }
                                        </Badge>
                                    )}
                                </div>
                                {data.data_appointment} - {data.hora} -{" "}
                                {data.medico}
                            </div>

                            <Button
                                disabled={data.estado === "closed"}
                                onClick={() =>
                                    handleCloseAppointment(data.id, index)
                                }
                            >
                                Fechar
                            </Button>
                        </ListGroup.Item>
                    ))}
                </ListGroup>
            </div>

            <Container>
                <h1>Reconhecimento facial de cliente</h1>
                <CameraFeed
                    addNotification={addNotification}
                    uploadTo="recognition/"
                    successHandler={handleFacialRecognitionResponse}
                />
            </Container>
        </div>
    );
};

export default AdminDashboard;
