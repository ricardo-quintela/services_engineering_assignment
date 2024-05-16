import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Badge, Button } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { NotificationData } from "../interfaces/notification";
import ListGroup from "react-bootstrap/ListGroup";
import { AppointmentData } from "../interfaces/appointment";

axios.defaults.withCredentials = true;

const AdminDashboard = ({
	addNotification,
}: {
	addNotification: (notificationData: NotificationData) => void;
}) => {
	const [appointmentData, setAppointmentData] = useState(
		[] as AppointmentData[]
	);

	if (appointmentData.length === 0) {
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
			})
			.catch(() =>
				addNotification({
					title: "Error",
					message: "Couldn't get appointments data.",
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
						title: "Error",
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
					title: "Error",
					message: "An error occured while closing the appointment.",
				})
			);
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
                                                    payed: "Paga"
                                                }[data.estado]

                                            }
										</Badge>
									)}
								</div>
								{data.horario.replace("|", " at ")} - {" "}
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

			<div className="d-flex gap-3 flex-sm-row flex-column flex-wrap w-50">
				<Card style={{ width: "18rem" }}>
					<Card.Body>
						<Card.Title>Reconhecimento Facial</Card.Title>
						<Card.Text>
							Verificar a consulta de um cliente através de
							software de reconhecimento facial.
						</Card.Text>
						<Button variant="primary">Ir</Button>
					</Card.Body>
				</Card>
			</div>
		</div>
	);
};

export default AdminDashboard;
