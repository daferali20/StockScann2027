import { useEffect } from "react";

export default function TradingViewChart({ symbol }) {

  useEffect(() => {

    const script = document.createElement("script");

    script.src =
      "https://s3.tradingview.com/tv.js";

    script.async = true;

    script.onload = () => {

      new window.TradingView.widget({
        autosize: true,
        symbol: symbol,
        interval: "5",
        timezone: "Etc/UTC",
        theme: "dark",
        style: "1",
        locale: "en",
        container_id: "tv_chart"
      });

    };

    document.body.appendChild(script);

  }, [symbol]);

  return (
    <div
      id="tv_chart"
      style={{
        height: "600px",
        width: "100%"
      }}
    />
  );
}
