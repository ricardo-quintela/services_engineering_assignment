import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FormEvent, useState } from "react";
import { Badge, Button } from "react-bootstrap";
import { NotificationData } from "../interfaces/notification";
import ListGroup from "react-bootstrap/ListGroup";
import { AppointmentData } from "../interfaces/appointment";
import { PaymentInfo } from "../interfaces/paymentInfoInterface";
import InfoPayment from "./InfoPayment"

axios.defaults.withCredentials = true;

const AppointementsDashboard = ({
	addNotification,
}: {
	addNotification: (notificationData: NotificationData) => void;
}) => {
	const [appointmentData, setAppointmentData] = useState(
		[] as AppointmentData[]
	);

	// Variável para decidir quando abre o menu de pagamento
	const [payment_window, setPaymentWindow] = useState(false);
	// Variável para guardar o ID da consulta
	const [appointmentId, setAppointmentId] = useState(-1);
	// Variável para decidir se abre o menu com as informações de pagamento
	const [paymentDocs, setPaymentDocs] = useState(false);
	// Variável para guardar as informações de pagamento
	const [infoPayment, setInfoPayment] = useState<PaymentInfo | null>(null);
	// Variável para pedir o numero de telemovel
	const [askTele, setAskTele] = useState(false);
	const [numTele, setNumTele] = useState(0);
	// Variável para guardar o index da consulta na tela
	const [indexSafe, setIndexSafe] = useState(-1);
	// Corre ao abrir a página
	const [ranQuery, setRanQuery] = useState(false);

	if (!ranQuery) {
		setRanQuery(true);
		axios
			.get(process.env.REACT_APP_API_URL + "appointments_list/")
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


	// Pedimos informações para ser possível proceder ao pagamento
	const handlePayAppointment = (optionId: number) => {

		const url = process.env.REACT_APP_API_URL + `payment/${optionId}/${numTele}`;
		console.log(url);

		axios
			.get(
				url
			)
			.then((response) => {
				if ("error" in response.data) {
					addNotification({
						title: "Error",
						message: response.data["error"],
					});
					return;
				}
				
				const paymentInfo: PaymentInfo = {
					  entidade: response.data.entidade ?? undefined,
					  referencia: response.data.referencia ?? undefined,
					  telemovel: response.data.telemovel ?? undefined,
					  valor: response.data.valor ?? undefined,
					};
				setInfoPayment(paymentInfo);
				setPaymentDocs(true);
				setNumTele(0);
				addNotification({
					title: "Success",
					message: "Please, procide with the payment.",
				})
			})
			.catch(() =>
				addNotification({
					title: "Error",
					message: "An error occured while closing the appointment.",
				})
			);
	};

	// Atualização da consulta
	const handleUpdateAppoitment = (appointmentId: number, index: number) => {

		setIndexSafe(-1);
		axios
            .put(
                process.env.REACT_APP_API_URL +
                    `appointments/${appointmentId}/`,
                { estado: "payed" }
            )
            .then((response) => {
                if ("error" in response.data) {
                    addNotification({
                        title: "Erro",
                        message: response.data["error"],
                    });
                    return;
                }

				addNotification({
                    title: "Success",
                    message: "Pago com sucesso.",
                })

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
								{data.data_appointment} - {" "}
								{data.hora} - {" "}
								{data.medico}
							</div>

							<Button
								disabled={data.estado === "payed" || data.estado === "closed"}
									onClick={() => {
										setAppointmentId(data.id);
										setIndexSafe(index);
										setPaymentWindow(!payment_window ? true : false);
									}
								}
							>
								Pagar
							</Button>
						</ListGroup.Item>
					))}
				</ListGroup>
			</div>
			{payment_window && 
				<div className="z-3 position-absolute p-5 rounded-3 top-50 start-50 translate-middle bg-body-secondary w-170 border">
				{!paymentDocs &&
					<>
					<h2 className="text-center"> Escolha o método de pagamento </h2>
					<div className="container overflow-hidden text-center mt-5">
						<div className="row g-3">
							<div className="col">
								<button type="button" className="btn btn-primary btn-bg" onClick={() => {
									setAskTele(true);
									setPaymentDocs(true);
								}}>
									MbWay
								</button>
							</div>
							<div className="col">
								<button type="button" className="btn btn-primary btn-bg" onClick={() =>  handlePayAppointment(2)}>
									Multibanco
								</button>					
							</div>
							<div className="col">
								<button type="button" className="btn btn-primary btn-bg" onClick={() =>  handlePayAppointment(3)}>
									Balcão
								</button>					
							</div>
						</div>	
					</div>
					</>
				}
				{askTele && 
					<>
					<h2 className="text-center"> Insira o seu número de telemóvel </h2>
					<div className="container overflow-hidden text-center mt-5">
						<form>
							<div className="row g-5">
								<div className="col">
									<input type="text" className="form-control" id="telemovel" onChange={(event) => setNumTele(Number(event?.target.value)) }/>
								</div>
								<div className="col">
									<button type="submit" className="btn btn-primary btn-bg" onClick={() => {
										setAskTele(false);
										handlePayAppointment(1);
										}}>
										Proceguir
									</button>					
								</div>
							</div>	
						</form>
					</div>
					</>
				}
				{(paymentDocs && !askTele) && 
				<>
				<h2 className="text-center"> Selecionou o método de pagamento. Use a seguinte informação: </h2>
				{infoPayment != null && 
					<InfoPayment 
						infoPayment={infoPayment}
					/>
				}
				<button type="button" className="btn btn-primary btn-bg" 
					onClick={() =>  
					{
						setPaymentWindow(false); 
						setPaymentDocs(false); 
						setInfoPayment(null); 
						handleUpdateAppoitment(appointmentId, indexSafe);
						}
					}
				>
					Pagamento Feito
				</button>					
				</>
			}
			</div>
			}
		</div>
	);
};

export default AppointementsDashboard;


// process.env.REACT_APP_API_URL +
//                     `appointments/${appointmentId}/`,
//                 { estado: "closed" }