import { useEffect, useState } from "react";

import {
  getBigTrades,
  getTopMoneyFlow
}
from "../services/api";

import BigTradesTable from "./BigTradesTable";
import TopFlowTable from "./TopFlowTable";
import TradingViewChart from "./TradingViewChart";

export default function Dashboard() {

  const [trades, setTrades] = useState([]);

  const [topFlow, setTopFlow] = useState([]);

  const [selectedSymbol,
          setSelectedSymbol] = useState("NASDAQ:AAPL");

  useEffect(() => {

    load();

    const timer = setInterval(
      load,
      1000
    );

    return () => clearInterval(timer);

  }, []);

  const load = async () => {

    const tradesData =
      await getBigTrades();

    const flowData =
      await getTopMoneyFlow();

    setTrades(tradesData);

    setTopFlow(flowData);

    if (flowData.length > 0) {

      setSelectedSymbol(
        `NASDAQ:${flowData[0].symbol}`
      );

    }

  };

  return (

    <div className="dashboard">

      <div className="left">

        <TopFlowTable
          rows={topFlow}
        />

        <BigTradesTable
          trades={trades}
        />

      </div>

      <div className="right">

        <TradingViewChart
          symbol={selectedSymbol}
        />

      </div>

    </div>

  );
}
