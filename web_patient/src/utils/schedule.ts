import {
    addDays,
    differenceInCalendarDays,
    differenceInCalendarWeeks,
    format,
    getHours,
    isSameDay,
    isSameWeek,
    startOfWeek,
} from 'date-fns';
import { IScheduledItem, KeyedMap } from 'shared/types';

// Default week starts on Monday

export const defaultDateFormat = 'MM/dd/yyyy';

export const isScheduledForDay = (item: IScheduledItem, date: Date) => {
    if (item.dueType == 'Week') {
        return isSameWeek(item.dueDate, date, {
            weekStartsOn: 1,
        });
    } else {
        return isSameDay(item.dueDate, date);
    }
};

export const getGreeting = (time: Date) => {
    const timeOfDay = getHours(time) % 24;

    if (timeOfDay < 6) {
        return 'Good night';
    } else if (timeOfDay < 12) {
        return 'Good morning';
    } else if (timeOfDay < 18) {
        return 'Good afternoon';
    } else {
        return 'Good evening';
    }
};

export const formatDayRelative = (date: Date, referenceDate: Date) => {
    const dateDiff = differenceInCalendarDays(date, referenceDate);

    if (dateDiff == 0) {
        return 'today';
    } else if (dateDiff == 1) {
        return 'tomorrow';
    } else if (dateDiff == -1) {
        return 'yesterday';
    } else {
        return `${format(date, defaultDateFormat)}`;
    }
};

export const getTaskItemDueTimeString = (item: IScheduledItem, referenceDate: Date) => {
    if (item.dueType == 'Week') {
        const weekDiff = differenceInCalendarWeeks(item.dueDate, referenceDate, {
            weekStartsOn: 1,
        });
        if (weekDiff == 0) {
            return 'due this week';
        } else if (weekDiff == 1) {
            return 'due next week';
        } else if (weekDiff == -1) {
            return 'due last week';
        } else if (weekDiff < -1) {
            return `due ${Math.abs(weekDiff)} weeks ago`;
        } else if (weekDiff > 1) {
            return `due in ${weekDiff} weeks`;
        }
    } else if (item.dueType == 'Day') {
        return `due ${formatDayRelative(item.dueDate, referenceDate)}`;
    } else if (item.dueType == 'ChunkOfDay') {
        const timeOfDay = getHours(item.dueDate) % 24;

        if (timeOfDay < 6) {
            return `due ${formatDayRelative(item.dueDate, referenceDate)} before morning`;
        } else if (timeOfDay < 12) {
            return `due ${formatDayRelative(item.dueDate, referenceDate)} in the morning`;
        } else if (timeOfDay < 18) {
            return `due ${formatDayRelative(item.dueDate, referenceDate)} in the afternoon`;
        } else {
            return `due ${formatDayRelative(item.dueDate, referenceDate)} in the evening`;
        }
    } else {
        return `due ${formatDayRelative(item.dueDate, referenceDate)} at ${format(item.dueDate, 'h:mm aaa')}`;
    }
};

export const groupTaskItemsByDay = (items: IScheduledItem[]) => {
    const groups: KeyedMap<IScheduledItem[]> = {};

    items.forEach((item) => {
        if (item.dueType == 'Week') {
            // If the item is due during the week, add it to every day of the week
            const start = startOfWeek(item.dueDate, { weekStartsOn: 1 });
            for (var i = 0; i < 7; i++) {
                const day = format(addDays(start, i), defaultDateFormat);
                groups[day] = groups[day] || [];
                groups[day].push(item);
            }
        } else {
            const day = format(item.dueDate, defaultDateFormat);
            groups[day] = groups[day] || [];
            groups[day].push(item);
        }
    });

    return groups;
};