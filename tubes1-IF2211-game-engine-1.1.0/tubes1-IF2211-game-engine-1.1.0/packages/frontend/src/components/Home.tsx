import axios from 'axios';
import { useEffect, useState } from 'react';
import { useBoard } from '../hooks/useBoard';
import { Board } from './Board';
import { BotScoreData } from './ScoreTable';
import { SideMenu } from './SideMenu';

export const Home = () => {
  const [boardId, setBoardId] = useState(1);
  const { board, bots } = useBoard(boardId, 250);
  const [finalScores, setFinalScores] = useState({});
  const [started, setStarted] = useState(false);
  const [botNames, setBotNames] = useState<Set<string>>(new Set());

  const onBoardChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setBoardId(parseInt(event.target.value));
  };

  useEffect(() => {
    bots.forEach((bot) => {
      if (!botNames.has(bot.name)) {
        setBotNames(new Set([...botNames, bot.name]));
      }
    });

    if (started) {
      if (bots.length == 0) {
        setStarted(false);
        const newFinalScore: { [key: string]: number } = {};
        for (const botName of [...botNames]) {
          const url = encodeURI(
            `/api/recordings/score/last?botName=${botName}`,
          );
          axios.get<number>(url).then((response) => {
            const score = response.data;
            console.log(`Bot name: ${botName}, bot score: ${score}`);
            newFinalScore[botName] = score;
          });
        }
        setFinalScores(newFinalScore);
      }
    } else {
      if (bots.length > 0) {
        setStarted(true);
        setFinalScores({});
        setBotNames(new Set());
      }
    }
  }, [bots]);

  return (
    <div className="bg-gray-50 dark:bg-gray-800 w-screen min-h-[70vh] flex flex-col my-5">
      <div className="flex-1 grid grid-cols lg:grid-cols-[1fr_30%] mx-4 gap-4 lg:mx-14 lg:p-0">
        <Board board={board} />
        <SideMenu
          bots={bots}
          boardId={boardId}
          onBoardChange={onBoardChange}
          botScores={getBotScoreData(finalScores)}
        />
      </div>
    </div>
  );
};

function getBotScoreData(finalScores: {
  [key: string]: number;
}): BotScoreData[] {
  const botScoreData: BotScoreData[] = [];
  for (const key in finalScores) {
    botScoreData.push({ name: key, score: finalScores[key] });
  }
  botScoreData.sort((a, b) => b.score - a.score);
  return botScoreData;
}
