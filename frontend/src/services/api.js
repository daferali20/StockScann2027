import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getBigTrades = async () => {
  const r = await API.get("/big-trades");
  return r.data;
};

export const getTopMoneyFlow = async () => {
  const r = await API.get("/top-money-flow");
  return r.data;
};
