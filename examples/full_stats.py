from yahoostats.evaluator import combine_stats
from yahoostats.logger import logger

stocklist = ['GOOGL', 'TSLA', 'AMD']
logger.info(f'Run full stats for {stocklist}')
print(combine_stats(stocklist, browser='Chrome'))
