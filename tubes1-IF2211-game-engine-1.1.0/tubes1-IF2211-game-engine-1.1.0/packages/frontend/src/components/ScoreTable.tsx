import { FC, memo } from 'react';
import { Table } from './Table';

export type BotScoreData = {
  name: string;
  score: number;
};

type PlayerTableProps = {
  botScores: BotScoreData[];
};

export const ScoreTable: FC<PlayerTableProps> = memo((props) => {
  const { botScores } = props;

  return (
    <Table label={`Final Score`} cols={['Name', 'Score']} data={botScores} />
  );
});
