import axios, { AxiosResponse } from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Badge, Button, Container } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { NotificationData } from "../interfaces/notification";
import ListGroup from "react-bootstrap/ListGroup";
import { AppointmentData } from "../interfaces/appointment";
import CameraFeed from "./CameraFeed";

axios.defaults.withCredentials = true;

const SIMILARITY_THRESHOLD = 90;

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

    const handleFacialRecognitionResponse = (response: AxiosResponse) => {
        const comparison_result =
            "message" in response.data
                ? response.data.message.comparison_result
                : null;

        if (comparison_result === null) {
            addNotification({
                title: "Erro",
                message: "Ocorreu um erro ao autenticar o cliente.",
            });
            return;
        }

        addNotification({
            title: "message" in response.data ? "Sucesso" : "Error",
            message:
                comparison_result >= SIMILARITY_THRESHOLD
                    ? "Cliente autenticado"
                    : "Cliente não foi reconhecido",
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
					aditionalFormInputs={[{inputLabel: "Nome de utilizador do cliente", inputField: <input id="username"/>}]}
                />
            </Container>
        </div>
    );
};

export default AdminDashboard;
