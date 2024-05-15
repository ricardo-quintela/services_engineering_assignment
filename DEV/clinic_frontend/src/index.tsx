import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import App_Schedulling from "./components/App_Schedulling";
import { BrowserRouter , Route, Routes, redirect } from "react-router-dom";
import App_Login from "./components/App";


const root = ReactDOM.createRoot(
    document.getElementById("root") as HTMLElement
);
root.render(
    <>
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<App_Schedulling />}></Route>
            <Route path="/Marcacao" element={<App_Schedulling />}></Route>
            <Route path="/Login" element={<App_Login />}></Route>
        </Routes>
    </BrowserRouter>
    </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();