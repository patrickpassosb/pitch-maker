import { Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { InputPage } from "@/pages/InputPage";
import { GeneratingPage } from "@/pages/GeneratingPage";
import { ResultPage } from "@/pages/ResultPage";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/generating/:jobId" element={<GeneratingPage />} />
        <Route path="/result/:jobId" element={<ResultPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
